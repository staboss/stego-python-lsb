#!/usr/bin/python3

import os
import time

from lsb import Lsb
from util import cmd_parser


def main():
    args = cmd_parser()

    coding = args.coding
    secret_message = args.message
    source_file = args.source_file
    result_file = args.result_file
    secret_file = args.secret_file

    # Input check
    if args.embed is True and args.message is None and args.secret_file is None:
        print("ERROR: Embedding requires a secret message!")
        return

    # Read the secret file, if it's specified
    if args.secret_file is not None:
        with open(secret_file, 'r') as text_file:
            secret_message = text_file.read().replace('\n', '')

    if coding is not None:
        try:
            coding = int(coding)
        except ValueError:
            print("ERROR: unsupported encoding format '" + coding + "'")
            return
    else:
        coding = 8

    # Embedding
    if args.embed:

        # Set the result file if it's not specified
        if not args.result_file:
            dir_name = os.path.dirname(os.path.normpath(source_file))
            result_file = dir_name + "/secret_image.bmp"

        res_name, res_extension = os.path.splitext(result_file)
        if res_extension != ".bmp":
            result_file = res_name + ".bmp"

        s_time = time.time()
        is_embedded = Lsb(source_file, coding).embed(secret_message, result_file)
        e_time = time.time()

        if is_embedded:
            print("Secret message was successfully embedded!\n")
            print("Time: " + f'{(e_time - s_time):.2f}' + " s")
        else:
            print("Something went wrong...")

    # Extracting
    else:
        s_time = time.time()
        secret = Lsb(source_file, coding).extract()
        e_time = time.time()

        print("Embedded message:\n" + secret + "\n")
        print("Time: " + f'{(e_time - s_time):.2f}' + " s")


if __name__ == '__main__':
    main()
