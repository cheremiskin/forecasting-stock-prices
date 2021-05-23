import yfinance as yf
import math
import matplotlib.pyplot as plt
import numpy as np

from walsh_function import Wal
from integral import integral, integral_sum
from format_data import format_data
from progress_bar import printProgressBar


# Данные акции
# data = yf.download('AAPL', '2020-04-01', '2021-04-01')
data = yf.download('AAPL', '2010-04-01', '2021-04-01')

stock_time, stock_price = format_data(data)
price = []

# T - период анализа (длительность сигнала)
T = len(stock_time)

# N - число функций Уолша в системе. N = 2^m
N = 128

# Мемоизированные значения с
c_memo = [None for i in range(N)]


def x(t):
    return stock_price[math.floor(t)]


def get_func(n, T):
    return lambda t: x(t) * Wal(n, t, T)


def c(n, T):
    return integral_sum(get_func(n, T), 0, T, eps=0.1) / T


def W(t, T):
    val = 0
    for n in range(N):
        val = val + c(n, T) * Wal(n, t, T)
    return val


for t in range(len(stock_time)):
    # printProgressBar(t, len(stock_time), prefix= 'Progress: ', length=50)
    price.append(W(t, T))

plt.plot(stock_time, stock_price, label="Цена акции")
plt.plot(stock_time, price, label="Графическая статистическая модель")
plt.legend()
# data['Adj Close'].plot()
plt.show()
