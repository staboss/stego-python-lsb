import cv2
import numpy as np

from math import log10, sqrt
from argparse import ArgumentParser

path_plt_pic = "resources/plot.png"
path_src_pic = "resources/src.bmp"
path_res_pic = "resources/res.bmp"

max_pixel = 255.0


def psnr(original, modified):
    pic_1 = cv2.imread(original)
    pic_2 = cv2.imread(modified, 1)

    mse = np.mean((pic_1 - pic_2) ** 2)
    if mse == 0:
        return 100

    psnr_value = 20 * log10(max_pixel / sqrt(mse))
    return float(f'{psnr_value:.2f}')


def cmd_parser():
    cmd = ArgumentParser(description="Embedding information in images (LSB Method)")

    # Extract data
    cmd.add_argument("-e", dest="embed", action="store_false",
                     help="extracting the secret message, embedding by default", default=True)

    # Secret message
    cmd.add_argument("-m", dest="message", required=False,
                     help="the secret message to embed")

    # Character storage
    cmd.add_argument("-b", dest="coding", required=False,
                     help="the number of bits for a symbol, 8 bits by default")

    # Source image file
    cmd.add_argument("-s", dest="source_file", required=True,
                     help="the name of the source file", metavar="FILE")

    # Result image file
    cmd.add_argument("-r", dest="result_file", required=False,
                     help="the name of the result file", metavar="FILE")

    # Secret message in the file
    cmd.add_argument("-f", dest="secret_file", required=False,
                     help="the text file containing the secret message", metavar="FILE")

    return cmd.parse_args()
