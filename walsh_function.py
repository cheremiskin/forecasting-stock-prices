import math
from scipy import integrate
from gray_code_builder import GrayCodeBuilder


def sign(x):
    if x == 0:
        return 0
    else:
        return x / abs(x)


def Rad(k, teta):
    if k == 0:
        return 1
    else:
        return sign(math.sin(pow(2, k) * math.pi * teta))
        

def Wal(n, t, T):
    if n == 0:
        return 1
    else:
        val = 1

        m = 0
        while pow(2, m) <= n:
            m += 1

        GrayCode = GrayCodeBuilder(m)
        for k in range(m):
            if GrayCode.gray_code[n][-(k + 1)] == 1:
                val *= Rad((k + 1), t/T)
        return val


def W(t, T, N, x):
    val = 0
    for n in range(N):
        val += c(n, t, T, x) * Wal(n, t, T)
    return val


def get_func(n, x, T):
    # return lambda t: x[int(t)] * Wal(n, t, T)
    return lambda t: Wal(n, t, T)


def c(n, t, T, x):
    # return integrate.quad(get_func(n, x, T), 0, T) / T
    return x[t] * integrate.quad(get_func(n, x, T), 0, T) / T

