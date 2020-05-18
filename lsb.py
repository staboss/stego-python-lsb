from PIL import Image

# The number of bits used to indicate the color of a single pixel in a bitmapped image
color_depth = {
    '1': 1,
    'L': 8, 'P': 8,
    'RGB': 24, 'YCbCr': 24,
    'RGBA': 32, 'CMYK': 32, 'F': 32, 'I': 32
}


class Lsb:
    """
    LSB replacement is a simple technique
    that involves swapping the least significant bit of
    each pixel's colour components with the bits of the message.
    """

    def __init__(self, image_path, bits=8):
        self.image_path = image_path
        self.bits_string = None
        self.container = None
        self.message = None
        self.bits = bits

    @staticmethod
    def change_lsb(component, bit):
        return (component & ~1) | int(bit)

    def binary_format(self, string):
        return list(map(lambda char: bin(ord(char))[2:].rjust(self.bits, '0'), string))

    def bit_per_pixel(self):
        if self.container is not None:
            return color_depth[self.container.mode]

    def open_container(self):
        try:
            self.container = Image.open(self.image_path)
            return True
        except FileNotFoundError:
            print("ERROR: File '" + self.image_path + "' does not exist!")
            return False

    def validate(self):
        """ Validates that the message can be embedded into the specified file """

        capacity = 0
        if self.open_container():
            capacity = self.container.width * self.container.height * (self.bit_per_pixel() / 8)

        self.bits_string = ''.join(self.binary_format(self.message))
        if len(self.bits_string) >= capacity:
            print("ERROR: The message is too long to be embedded in the specified image '" + self.image_path + "'!")
            return False

        return True

    def embed(self, secret_message, result_filename):
        """ Iterating through each pixel in the image and embedding the secret message """

        # Add message length
        self.message = str(len(secret_message)) + ':' + secret_message

        if not self.validate():
            print("ERROR: Validation failed. It is impossible to embed the message into this image!")
            return False

        stego_container = self.container.copy()
        width, height = self.container.size

        index = 0
        for y in range(height):
            for x in range(width):
                if index + 1 <= len(self.bits_string):
                    r, g, b = stego_container.getpixel((x, y))

                    # New 'RED' value
                    r = self.change_lsb(r, self.bits_string[index])

                    # New 'GREEN' value
                    if index + 2 <= len(self.bits_string):
                        g = self.change_lsb(g, self.bits_string[index + 1])

                    # New 'BLUE' value
                    if index + 3 <= len(self.bits_string):
                        b = self.change_lsb(b, self.bits_string[index + 2])

                    # New pixel value
                    stego_container.putpixel((x, y), (r, g, b))
                else:
                    break
                index += 3
        stego_container.save(result_filename)
        return True

    def extract(self):
        """ Iterating through each pixel in the image and extracting the secret message """

        if not self.open_container():
            return ""

        width, height = self.container.size

        buffer = 0
        counter = 0

        message_bits = []
        message_size = None

        for y in range(height):
            for x in range(width):

                # Iterating through each RGB component and pull out the LSB
                for component in self.container.getpixel((x, y)):

                    # Read the bit and shift left to make a bit chunk
                    buffer += (component & 1) << (self.bits - 1 - counter)
                    counter += 1

                    # Convert a bit chunk to char and append it
                    if counter == self.bits:
                        message_bits.append(chr(buffer))

                        # Reset values
                        counter = buffer = 0

                        # If we get the separator for the first time, set the message size
                        if message_bits[-1] == ':' and message_size is None:
                            try:
                                message_size = int("".join(message_bits[:-1]))
                            except ValueError:
                                pass

                # Return a message when the read bits match the size of the message
                if len(message_bits) - len(str(message_size)) - 1 == message_size:
                    return "".join(message_bits)[len(str(message_size)) + 1:]

        return ""
