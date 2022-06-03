import warnings

from ForecastingMethods.ForecastingModel import ForecastingModelInterface
from Plot import Plot
from StationarityMethods.KPSSStationarity import KPSSStationarity
import pandas as pd
import numpy as np


def least_square_method(A, b):
    A, b = np.array(A), np.array(b)
    try:
        x = np.linalg.inv(A.T.dot(A)).dot(A.T).dot(b)
    except np.linalg.LinAlgError:
        x = np.linalg.pinv(A).dot(b)
    finally:
        return x


class ARIMA:
    def __init__(self, p, d, q, series):
        self.p = p
        self.d = d
        self.q = q

        self.num_coefficients = p + q + 1
        self.num_rows = len(series) - max(p, q) - 2

        self.coefficients = np.zeros(self.num_coefficients)

        self.series = series
        self.diff_series = self.diff(pd.DataFrame(self.series))

        self.errors = self.get_errors()

    def diff(self, series):
        d = BoxJenkinsMethod(self.series).calculate_d()

        for i in range(d):
            series = series.diff()
            series = pd.DataFrame([x for x in series[0].tolist() if str(x) != "nan"])

        return series[0].tolist()

    def get_errors(self):
        x = np.ones((len(self.diff_series) - 1, 2))
        x[:, 1] = self.diff_series[: len(self.diff_series) - 1]
        y = self.diff_series[1:]
        b = least_square_method(x, y)

        return y - x.dot(b)

    @staticmethod
    def get_lag_matrix(num_rows: int, num_cols: int, data: list[float]):
        matrix = np.zeros((num_rows, num_cols))

        for i in range(num_rows):
            for j in range(num_cols):
                matrix[i][j] = data[-j - i - 1]

        return matrix

    def forecast(self):
        self.fit()

        next_increment = np.dot(
            self.coefficients,
            np.concatenate(([0], self.diff_series[-self.p :], self.errors[-self.q :])),
        )

        return next_increment + self.series[-1]

    def fit(self):
        errors_matrix = self.get_lag_matrix(
            num_rows=self.num_rows, num_cols=self.q, data=self.errors
        )

        series_matrix = self.get_lag_matrix(
            num_rows=self.num_rows, num_cols=self.p, data=self.diff_series[:-1]
        )

        matrix = np.concatenate(
            (
                np.ones((self.num_rows, 1)),
                series_matrix,
                errors_matrix,
            ),
            axis=1,
        )

        self.coefficients = least_square_method(
            matrix, self.diff_series[-self.num_rows :]
        )


class BoxJenkinsMethod:
    def __init__(self, series: list[float], max_d=5, max_p=5, max_q=5):
        self.series = series

        self.max_d = max_d
        self.max_p = max_p
        self.max_q = max_q

        self.d = 0

        self.aic_matrix = [[]] * max_q
        for i in range(max_q):
            self.aic_matrix[i] = [-1] * max_p

    def calculate_d(self):
        series = pd.DataFrame(self.series)

        while (
            not KPSSStationarity.isStationarity(series[0].tolist())
            and self.d <= self.max_d
        ):
            self.d += 1
            series = series.diff()
            series = pd.DataFrame([x for x in series[0].tolist() if str(x) != "nan"])

        if self.d > self.max_d:
            warnings.warn("BoxJenkinsMethod.calculate_d: d > max_d")

        return self.d

    def calculate_aic_matrix(self):
        for q in range(self.max_q):
            for p in range(self.max_p):
                print("p:", p, ", q:", q)
                if p < 1 or q < 1:
                    continue
                train_data = self.series[: round(len(self.series) * 0.9)]
                test_data = self.series[len(train_data) :]

                forecast_data = []
                last_data = train_data.copy()

                for i in test_data:
                    forecast_data.append(ARIMA(p, 1, q, last_data).forecast())
                    last_data.append(i)

                mse = mean_squared_error(forecast_data, test_data)
                if mse < min_mse:
                    min_mse = mse
                    pp = p
                    qq = q
                    forecast = forecast_data
