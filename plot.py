import matplotlib.pyplot as plt
import numpy as np

from walsh_function import Wal, Rad


def show_wal():
    T = 1000
    plt.figure(figsize=(14, 7))
    plt.subplots_adjust(wspace=0.35, top=0.94, hspace=0.56)
    t = np.linspace(0, T, 1000)

    for i in range(16):
        w = list(map(lambda ti: Wal(i, ti, T), t))
        plt.subplot(4, 4, i+1)
        plt.plot(t, w)
        plt.title("W" + str(i))
        # plt.ylabel("w" + str(i), fontsize=14)  # ось ординат
        plt.grid(True)  # включение отображение сетки

    plt.show()


show_wal()