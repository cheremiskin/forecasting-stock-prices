import math

# from GreyCodeBuilder import GrayCodeBuilder
# from Integral import integral_sum
import MathUtils
from GreyCodeBuilder import GreyCodeBuilder


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

        gray_code = GreyCodeBuilder(m).get_code()
        for k in range(m):
            if gray_code[n][-(k + 1)] == 1:
                val *= Rad((k + 1), t / T)
        return val


# def W(t, T, N, c_memo):
#     val = 0
#     for n in range(N):
#         val += c_memo[n] * MathUtils.Walsh(n, t, T)
#         # val += c_memo[n] * Wal(n, t, T)
#     return val


def W(t, T, N, c_memo, w_t, last_n_t):
    print(w_t, last_n_t)

    for n in range(last_n_t[t], N):
        w_t[t] += c_memo[n] * MathUtils.Walsh(n, t, T)
        # val += c_memo[n] * Wal(n, t, T)
    return w_t[t], w_t, last_n_t


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
    return MathUtils.integral(get_func(n, x, T), 0, T) / T
