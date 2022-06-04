import math
from typing import Type

from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

from ForecastingMethods.ForecastingModel import ForecastingModelInterface


class PerformanceEvaluationForecastingModel:
    data: list[float]
    train_set: list[float]
    validation_set: list[float]

    forecast: list[float] = []

    def __init__(
        self,
        model,
        data: list[float],
        train_ratio: float = 0.9,
    ):
        self.split_data(data=data, train_ratio=train_ratio)
        self.model = model
        if model is not None:
            self.generate_forecast()

    def split_data(self, data: list[float], train_ratio: float):
        train_set_size = math.ceil(len(data) * train_ratio)

        self.train_set = data[:train_set_size]
        self.validation_set = data[train_set_size:]

    def get_chat_data(self):
        return [self.forecast, self.validation_set]

    def generate_forecast(self):
        self.forecast = []

        trained_model = self.model(data=self.train_set)
        trained_model.fit()

        accumulated_data = self.train_set

        for i in self.validation_set:
            self.forecast.append(trained_model.forecast(accumulated_data)[0])
            accumulated_data.append(i)

    def get_mse(self):
        return mean_squared_error(self.forecast, self.validation_set)

    def show_criteria(self):
        acc_err = 0
        ma = 0
        mae = 0
        mape = 0
        err_percent = []
        for i in range(len(self.forecast)):
            ma += self.forecast[i] - self.validation_set[i]
            abs_err = abs(self.forecast[i] - self.validation_set[i])
            acc_err += abs_err
            mae += abs_err
            mape += abs_err / self.validation_set[i] * 100
            err_percent.append(abs_err * 100 / self.validation_set[i])

        acc_err /= len(self.forecast)
        ma /= len(self.forecast)
        mae /= len(self.forecast)
        mape /= len(self.forecast)

        print("mse: ", mean_squared_error(self.forecast, self.validation_set))
        print("ma:", ma)
        print("mae:", mae)
        print("mape:", mape)
