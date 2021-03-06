import math
import json
from typing import Callable

import yfinance as yf
import matplotlib.pyplot as plt

from format_data import format_data
from walsh_function import c, W
from progress_bar import printProgressBar


def get_sigma(x: Callable[[float], float],
              W: Callable[[int, int, int, list], float],
              T: int,
              N: int,
              c_memo: list):
    sigma = 0
    for t in range(T):
        sigma += pow(x(t) - W(t, T, N, c_memo), 2) / T
    return sigma


if __name__ == '__main__':
    INPUT_FILE_NAME = 'input.json'
    CONFIG_FILE_NAME = 'config.json'

    with open(INPUT_FILE_NAME) as f:
        input_data = json.load(f)
        try:
            ticker, start_period, end_period = (i[1] for i in input_data.items())
        except Exception:
            raise Exception("Не удалось прочесть входные данные")

    with open(CONFIG_FILE_NAME) as f:
        config_data = json.load(f)
        try:
            N_max, = (i[1] for i in config_data.items())  # Максимальное кол-во функций Уолша
        except Exception:
            raise Exception("Не удалось прочесть входные данные")

    # Получение данных
    stock_data = yf.download(ticker, start_period, end_period)
    stock_time, stock_price = format_data(stock_data)

    N_max = min(N_max, int(len(stock_time) / 2))
    N_opt = None  # Оптимальное число функций Уолша
    T = len(stock_time)  # Период анализа (длительность сигнала)
    c_memo = [None for i in range(N_max + 1)]  # Мемоизированные значения с
    sigma = [None for i in range(N_max + 1)]  # Массив погрешностей

    # Подсчет коэффициентов Уолша - c
    n = 0
    while n <= N_max:
        printProgressBar(n, N_max, prefix='Вычисление коэффициентов Уолша: ', length=50)
        c_memo[n] = c(n, T, lambda te: stock_price[math.floor(te)])
        n += 1

    # Подбор кол-ва функций Уолша - N
    n: int = 10
    while n <= N_max:
        sigma[n] = get_sigma(lambda te: stock_price[math.floor(te)], W, T, n, c_memo)
        printProgressBar(n, N_max, prefix='Вычисление суммарного среднеквадратичного отклонения: ', length=50)
        n += 10

    min_sigma = None
    for i in range(N_max):
        printProgressBar(i, N_max, prefix='Подбор оптимального числа функций Уолша: ', length=50)
        if sigma[i] is not None:
            if min_sigma is None or min_sigma > sigma[i]:
                min_sigma = sigma[i]
                N_opt = i

    printProgressBar(N_max, N_max, prefix='Подбор оптимального числа функций Уолша: ', length=50)
    # Построение модели
    price = []
    for t in range(len(stock_time)):
        price.append(W(t, T, N_opt, c_memo))

    price[0] = stock_price[0]
    # Построение графиков
    plt.subplot(2, 1, 1)
    plt.plot(stock_time, stock_price, label="Цена акции")
    plt.title("исходный сигнал")
    plt.subplot(2, 1, 2)
    plt.plot(stock_time, price, label="Графическая статистическая модель")
    plt.title("графическая статичтическая модель")
    plt.show()
