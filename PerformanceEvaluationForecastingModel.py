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
        model: Type[ForecastingModelInterface],
        data: list[float],
        train_ratio: float = 0.9,
    ):
        self.split_data(data=data, train_ratio=train_ratio)
        self.model = model
        self.generate_forecast()

    def split_data(self, data: list[float], train_ratio: float):
        train_set_size = math.ceil(len(data) * train_ratio)

        self.train_set = data[:train_set_size]
        self.validation_set = data[train_set_size:]

    def generate_forecast(self):
        accumulated_data = self.train_set
        trained_model = self.model(self.train_set)

        for i in self.validation_set:
            self.forecast.append(trained_model.forecast(accumulated_data)[0])
            accumulated_data.append(i)

        acc_err = 0
        err_percent = []
        for i in range(len(self.forecast)):
            abs_err = abs(self.forecast[i] - self.validation_set[i])
            acc_err += abs_err
            err_percent.append(abs_err * 100 / self.validation_set[i])

        acc_err /= len(self.forecast)

        print("mse: ", mean_squared_error(self.forecast, self.validation_set))
        print("acc_err:", acc_err)
        print("max err percent:", max(err_percent))
        print("min err percent:", min(err_percent))
        print("average err percent:", sum(err_percent) / len(err_percent))

        plt.plot(self.train_set + self.forecast, label="Forecast")
        plt.plot(self.train_set + self.validation_set, label="Original")
        plt.legend()
        plt.show()
