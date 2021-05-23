import math
from gray_code_builder import GrayCodeBuilder
from integral import integral_sum


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


def W(t, T, N, c_memo):
    val = 0
    for n in range(N):
        val += c_memo[n] * Wal(n, t, T)
    return val


def get_func(n, x, T):
    # return lambda t: x[int(t)] * Wal(n, t, T)
    return lambda t: x(t) * Wal(n, t, T)


def c(n, T, x):
    """

    :param n: номер коэффициента
    :param T: длина сигнала
    :param x:
    :return:
    """
    return integral_sum(get_func(n, x, T), 0, T, eps=0.1) / T

