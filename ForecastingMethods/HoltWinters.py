import math

import numpy as np
from sklearn.metrics import mean_squared_error

from ForecastingMethods.ForecastingModel import ForecastingModelInterface
from MathUtils import least_square_method
from PerformanceEvaluationForecastingModel import PerformanceEvaluationForecastingModel


class HoltWinters(ForecastingModelInterface):
    def __init__(self, data, s=12, coefficients=None):
        super().__init__(data)

        if coefficients is None:
            coefficients = [0.1, 0.1, 0.1]
        self.alpha, self.betta, self.gamma = coefficients

        self.isFit = False

        self.data = data
        self.s = s

        self.L = []
        self.T = []
        self.S = []

        self.forecast_data = []

    def fit(self):
        first_l, first_t = self.get_initial_coefficients()

        self.L = [first_l]
        self.T = [first_t]
        self.S = [1] * self.s

        for t in range(1, len(self.data)):
            self.L.append(
                self.alpha * self.data[t] / self.S[max(0, t - self.s)]
                + (1 - self.alpha) * (self.L[t - 1] + self.T[t - 1])
            )
            self.T.append(
                self.betta * (self.L[t] - self.L[t - 1])
                + (1 - self.betta) * self.T[t - 1]
            )

            if t > self.s:
                self.S.append(
                    self.gamma * self.data[t] / self.L[t]
                    + (1 - self.gamma) * self.S[t - self.s]
                )

            self.forecast_data.append(
                (self.L[t - 1] + self.T[t - 1]) * self.S[max(0, t - self.s)]
            )

        self.isFit = True

    def get_initial_coefficients(self):
        ar_data = np.ones((self.s, 2))
        ar_data[:, 1] = [x for x in range(1, self.s + 1)]

        return least_square_method(ar_data, self.data[: self.s])

    def forecast(self, last_values: list[float] = None) -> list[float]:
        if self.S[-self.s] is None:
            print(self)
        l = self.alpha * last_values[-1] / self.S[-self.s] + (1 - self.alpha) * (
            self.L[-1] + self.T[-1]
        )
        self.L.append(l)

        self.T.append(
            self.betta * (self.L[-1] - self.L[-2]) + (1 - self.betta) * self.T[-1]
        )

        self.S.append(
            self.gamma * self.forecast_data[-1] / self.L[-1]
            + (1 - self.gamma) * self.S[-self.s]
        )

        self.forecast_data.append((self.L[-1] + self.T[-1]) * self.S[-self.s + 1])
        return [self.forecast_data[-1]]


class HoltWintersForecast(ForecastingModelInterface):
    def __init__(self, data):
        super().__init__(data)
        self.alpha = 0
        self.betta = 0
        self.gamma = 0
        self.step_size = 0.2
        self.min_mse = 1000000000
        self.model = None

    def fit(self):
        alpha = self.step_size
        while alpha < 1:
            betta = self.step_size
            while betta < 1:
                gamma = self.step_size
                while gamma < 1:
                    mse = self.check_model_mse(
                        coefficients=[round(alpha, 3), round(betta, 3), round(gamma, 3)]
                    )
                    if mse < self.min_mse:
                        self.alpha = alpha
                        self.betta = betta
                        self.gamma = gamma
                        self.min_mse = mse
                    gamma += self.step_size
                betta += self.step_size
            alpha += self.step_size

        self.model = HoltWinters(
            self.data, coefficients=[self.alpha, self.betta, self.gamma]
        )
        self.model.fit()

    def check_model_mse(self, coefficients):
        train_data = self.data[: round(len(self.data) * 0.9)]
        validation_data = self.data[len(train_data) :]

        hw = HoltWinters(train_data, coefficients=coefficients)
        hw.fit()

        forecast = []

        accumulated_data = train_data

        for i in validation_data:
            forecast.append(hw.forecast(accumulated_data)[0])
            accumulated_data.append(i)

        return mean_squared_error(forecast, validation_data)

    def forecast(self, last_values: list[float] = None) -> list[float]:
        return self.model.forecast(last_values)
