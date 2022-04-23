import math
from typing import Callable
from GrayCodeBuilder import GrayCodeBuilder


def sign(x: float):
    if x == 0:
        return 0
    else:
        return x / abs(x)


def Rad(n: int, t: float):
    """Rademacher function r_n(t)"""
    assert n >= 0, "n ∈ N"
    assert 0 <= t <= 1, "t ∈ [0, 1]"

    return sign(math.sin(pow(2, n) * math.pi * t))


def WalshCoefficient(
    x: Callable[[float], float], n: int, gray_code_builder: GrayCodeBuilder, T: int
):
    def func(t: float):
        return x(t) * Walsh(n=n, t=t / T, gray_code_builder=gray_code_builder)

    return integral(f=func, a=0, b=T, n=T) / T


def get_pow_of_2_greater_number(n: int):
    m = 0
    while pow(2, m) <= n:
        m += 1
    return m


def Walsh(n: int, t: float, gray_code_builder: GrayCodeBuilder):
    """Walsh function"""
    assert n >= 0, "n ∈ N"
    assert 0 <= t <= 1, "t ∈ [0, 1]"

    result = 1
    if n == 0:
        return result

    m = get_pow_of_2_greater_number(n)

    gray_code = gray_code_builder.get_code()

    for k in range(m):
        if gray_code[n][-(k + 1)] == 1:
            result *= Rad((k + 1), t)

    return result


def integral(f: Callable[[float], float], a: float, b: float, n: int = 100):
    """
    Calculation of the integral by the method of rectangles
    """
    result: float = 0
    h: float = (b - a) / n

    for i in range(n):
        result += f(a + h * (i + 0.5))

    result *= h

    return result
