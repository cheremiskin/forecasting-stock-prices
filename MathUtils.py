import math
from typing import Callable

from GreyCodeBuilder import GreyCodeBuilder


def sign(x: float):
    if x == 0:
        return 0
    else:
        return x / abs(x)


def Rad(k, t):
    """Функция Радемахера"""
    if k == 0 or t == 0:
        return 1
    else:
        return sign(math.sin(pow(2, k) * math.pi * t))


def Walsh(n, t, T):
    """Функция Уолша"""
    result = 1

    if n == 0:
        return result

    m = 0
    while pow(2, m) <= n:
        m += 1

    grey_code = GreyCodeBuilder(m).get_code()

    for k in range(m):
        if grey_code[n][-(k + 1)] == 1:
            result *= Rad((k + 1), t / T)
    return result


def integral(f: Callable[[float], float], a: float, b: float, n: int = 100):
    """
    Вычисление интеграла по методу средних прямоугольников
    """
    result: float = 0
    h: float = (b - a) / n

    for i in range(n):
        result += f(a + h * (i + 0.5))

    result *= h
    return result


def standard_deviation(
    values: Callable[[float], float],
    approximate_values: Callable[[float], float],
    n: int,
):
    sd = 0
    for i in range(n):
        sd += pow(values(i) - approximate_values(i), 2)

    return math.sqrt(sd / n)
