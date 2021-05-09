import yfinance as yf
import math
from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np
from walsh_function import W, Wal

data = yf.download('AAPL', '2020-04-01', '2021-04-01')

T = 5
N = 8
print(data['Adj Close'][0])


def x(t):
    return data['Adj Close'][math.floor(t)]


def get_func(n, T):
    # return lambda t: x[int(t)] * Wal(n, t, T)
    return lambda t: x(t) * Wal(n, t, T)


def c(n, T):
    return integrate.quad(get_func(n, T), 0, T)


def W(t, T):
    val = 0
    for n in range(N):
        # print(c(n,T))
        val = val + c(n, T)[0] * Wal(n, t, T)
    return val

price = []
time = np.linspace(0, data.size, 1000)

for t in range(data.size):
    price.append(W(t, T))
    # time.append(x(t))
# print(W(0, 5))

# plt.plot(time, price)
print(price[0], time[0])
# data['Adj Close'].plot()
# plt.show()
