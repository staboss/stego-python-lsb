from util import *
from lsb import Lsb
from matplotlib import pyplot as plot

x, y = [], []


def create_data():
    lsb = Lsb(image_path=path_src_pic)
    text = ""
    for word_counter in range(1001):
        text += "text "
        lsb.embed(text, path_res_pic)
        x.append(psnr(path_src_pic, path_res_pic))
        y.append(word_counter)


def create_plot():
    create_data()

    fig, axs = plot.subplots()

    axs.plot(x, y)
    axs.grid()

    plot.xlabel("PSNR")
    plot.ylabel("Word counter")

    fig.set_figwidth(12)
    fig.set_figheight(9)


def main():
    create_plot()
    plot.savefig(path_plt_pic, bbox_inches='tight')


if __name__ == '__main__':
    main()
