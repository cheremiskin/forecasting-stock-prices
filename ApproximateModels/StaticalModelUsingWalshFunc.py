import math
from typing import Callable

from sklearn.metrics import mean_squared_error

import MathUtils
from GrayCodeBuilder import GrayCodeBuilder


class StaticalModelUsingWalshFunc:
    gray_code_builder: GrayCodeBuilder

    # Restrictions on the number of Walsh functions in the system
    max_num_walsh_func: int
    min_num_walsh_func: int

    opt_num_of_walsh_func: int  # Optimal number of Walsh functions in the system
    minimal_mse: float  # Minimal mean squared error

    statical_models: list[list[float]]
    walsh_coefficients: list[float]

    T: int  # Signal length
    get_value: Callable[[float], float]  # Function to get the values of the signal

    def __init__(
        self,
        data: list[float],
        min_num_walsh_func: int = 1,
        max_num_walsh_func: int = 400,
    ):
        self.data = data

        self.min_num_walsh_func = min_num_walsh_func
        self.max_num_walsh_func = max_num_walsh_func

        self.T = len(data)
        self.get_value = lambda x: data[math.floor(x)]

    def generate_gray_code(self):
        m = MathUtils.get_pow_of_2_greater_number(self.max_num_walsh_func)
        self.gray_code_builder = GrayCodeBuilder(m)

    def calculate_walsh_coefficients(self):
        self.walsh_coefficients = [0] * self.max_num_walsh_func

        for n in range(self.max_num_walsh_func):
            self.walsh_coefficients[n] = MathUtils.WalshCoefficient(
                x=self.get_value,
                n=n,
                gray_code_builder=self.gray_code_builder,
                T=self.T,
            )

    def calculate_statical_model(self):
        self.statical_models = [[]] * self.max_num_walsh_func

        for n in range(self.max_num_walsh_func):
            self.statical_models[n] = [0] * self.T
            for t in range(self.T):
                if n == 0:
                    prev = 0
                else:
                    prev = self.statical_models[n - 1][t]

                self.statical_models[n][t] = prev + self.walsh_coefficients[
                    n
                ] * MathUtils.Walsh(
                    n=n, t=t / self.T, gray_code_builder=self.gray_code_builder
                )

    def choose_optimal_num_walsh(self):
        self.opt_num_of_walsh_func = self.min_num_walsh_func
        self.minimal_mse = mean_squared_error(
            self.data,
            self.statical_models[self.min_num_walsh_func],
        )

        for n in range(self.min_num_walsh_func + 1, self.max_num_walsh_func):
            mse = mean_squared_error(self.data, self.statical_models[n])
            if mse < self.minimal_mse:
                self.minimal_mse = mse
                self.opt_num_of_walsh_func = n

    def get_model(self) -> list[float]:
        self.generate_gray_code()
        self.calculate_walsh_coefficients()
        self.calculate_statical_model()
        self.choose_optimal_num_walsh()

        return self.statical_models[self.opt_num_of_walsh_func]