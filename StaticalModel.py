import math
import pandas as pd
import matplotlib.pyplot as plt
import MathUtils


class StandardDeviationForN:
    def __init__(self, value, n):
        self.n = n
        self.value = value


class StaticalModel:
    def __init__(self, data: pd.DataFrame):
        # Максимальное кол-во функций Уолша в модели
        self.n_max: int = 400

        # Опитмальное кол-во функций Уолша в модели
        self.n_optimal: int = 0

        # Период анализа (длительность сигнала)
        self.T: int = len(data)

        # Мемоизированные значения коэффициентов Уолша
        self.c_memo = [0 for _ in range(self.n_max + 1)]

        self.w_t = [0 for _ in range(self.T)]

        # Квадратичные отклоения для каждого кол-ва функций Уолша
        self.sigma = [0 for _ in range(self.n_max + 1)]

        # Массив дат исходного сигнала
        # self.dates = data["Date"].tolist()

        # Массив значений исходного сигнала
        self.values = data["Value"].tolist()

        # Массив значений статистической модели
        self.statical_model_values = []

        # Массив среднеквадратичных отклонений
        self.standard_deviations: list[StandardDeviationForN] = []

    def get_statical_model_value(self, t, N):
        result = 0
        for n in range(N):
            result += self.c_memo[n] * MathUtils.Walsh(n, t, self.T)
        return result

    def get_value(self, t):
        return self.values[math.floor(t)]

    def get_walsh_coefficient(self, n):
        def in_function(t):
            return self.get_value(t) * MathUtils.Walsh(n, t, self.T)

        return MathUtils.integral(f=in_function, a=0, b=self.T) / self.T

    def calculate_walsh_coefficients(self):
        """Вычисление коэффициентов Уолша для исходного сигнала"""

        print("-- calculate_walsh_coefficients b --")
        for n in range(self.n_max + 1):
            self.c_memo[n] = self.get_walsh_coefficient(n)
        print(self.c_memo)
        print("-- calculate_walsh_coefficients e --")

    def calculate_standard_deviation(self):
        """Вычисление среднеквадратичного отклонения для разного количества функций Уолша в системе"""

        print("-- calculate_standard_deviation b --")
        n: int = 10

        plt.plot([t for t in range(self.T)], self.values)

        while n <= self.n_max:

            if n < self.n_max:
                for t in range(len(self.w_t)):
                    for ni in range(n, n + 10):
                        self.w_t[t] += self.c_memo[ni] * MathUtils.Walsh(ni, t, self.T)

            if n == 10:
                print(self.w_t)
                plt.plot([t for t in range(self.T)], self.w_t)

            sd = MathUtils.standard_deviation(
                values=self.get_value,
                approximate_values=lambda t: self.w_t[t],
                n=self.T,
            )

            self.standard_deviations.append(
                StandardDeviationForN(
                    value=sd,
                    n=n,
                )
            )

            # print(n, sd)

            n += 10

        self.standard_deviations.sort(key=lambda i: i.value)
        self.n_optimal = self.standard_deviations[0].n
        print("res", self.n_optimal)
        plt.show()

        print("-- calculate_standard_deviation e --")

    def train(self):
        print("-- train b --")
        self.calculate_walsh_coefficients()
        self.calculate_standard_deviation()
        print("-- train e--")

    def create_statical_model(self):
        self.train()
        for t in range(self.T):
            self.statical_model_values.append(
                self.get_statical_model_value(t, self.n_optimal)
            )

        return self.statical_model_values
        # return pd.DataFrame(
        #     list(zip(self.dates, self.statical_model_values)), columns=["Date", "Value"]
        # )
