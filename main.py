import math
from random import random

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

from DataLoader import DataLoader
from ForecastingMethods.ARIMA import BoxJenkinsMethod, ARIMA
from ForecastingMethods.HoltWinters import HoltWintersForecast
from ForecastingMethods.MarkovChain import MarkovChain
from PerformanceEvaluationForecastingModel import PerformanceEvaluationForecastingModel
from Plot import Plot
import matplotlib.pyplot as plt
from StationarityMethods.KPSSStationarity import KPSSStationarity


def data_formatter(data: pd.DataFrame):
    data = data.filter(["Adj Close"], axis=1)
    data = data.rename(columns={"Adj Close": "Value"})
    data["Date"] = data.index
    return data


###########


def integration(data, d):
    if d == 0:
        return data
    data_ = data
    for _ in range(d):
        integr_data = np.empty(len(data_) - 1)
        for i in range(len(data_) - 1):
            integr_data[i] = data_[i + 1] - data_[i]
        data_ = integr_data
    return integr_data


def lag_data(data, lag):
    lag_matrix = np.zeros((len(data), lag))
    for l in range(lag):
        for i in range(len(data)):
            if not (i - l - 1) < 0:
                lag_matrix[i, l] = data[i - l - 1]
    return lag_matrix


def least_square_method(x, y):
    x, y = np.array(x), np.array(y)
    try:
        b = np.linalg.inv(x.T.dot(x)).dot(x.T).dot(y)
    except np.linalg.LinAlgError:
        b = np.linalg.pinv(x).dot(y)
    finally:
        return b


def show_trend():
    values = [x * 0.7 + random() ** 2 * 10 for x in range(100)]
    print(values)
    plt.plot(values, label="Seasonality")
    plt.plot([x * 0.7 for x in range(100)])
    plt.show()


def show_noise():
    noise = np.random.randn(250) * 100
    plt.plot(noise)
    plt.show()


def show_seasonality():
    time = np.arange(50)
    values = np.where(time < 10, time**3, (time - 9) ** 2)
    # Repeat the pattern 5 times
    seasonal = []
    for i in range(5):
        for j in range(50):
            seasonal.append(values[j])
    # Plot
    noise = np.random.randn(250) * 100
    seasonal += noise
    time_seasonal = np.arange(250)
    plt.plot(time_seasonal, seasonal, label="Seasonality")
    plt.show()


if __name__ == "__main__":
    test_data = [
        {
            "ticker": "SBUX",
            "start_period": "2015-04-01",
            "end_period": "2018-09-01",
        },
        {
            "ticker": "AAPL",
            "start_period": "2010-04-01",
            "end_period": "2021-09-01",
        },
        {
            "ticker": "GE",
            "start_period": "2013-04-01",
            "end_period": "2016-09-01",
        },
        {
            "ticker": "GAZP.ME",
            "start_period": "2015-04-01",
            "end_period": "2020-04-01",
        },
    ]

    show_trend()

    # fig, axs = plt.subplots(2, 2)
    # for i in range(len(test_data)):
    #     default_data = test_data[i]
    #
    #     data_loader = DataLoader(
    #         ticker=default_data["ticker"],
    #         start_period=default_data["start_period"],
    #         end_period=default_data["end_period"],
    #     )
    #
    #     stock_data: pd.DataFrame = data_loader.get_data(data_formatter=data_formatter)
    #     stock_data_list = stock_data["Value"].tolist()
    #
    #     pefm = PerformanceEvaluationForecastingModel(
    #         HoltWintersForecast, data=stock_data_list
    #     )
    #     chart_data = pefm.get_chat_data()
    #     print(default_data["ticker"])
    #     pefm.show_criteria()
    #
    #     axs[i % 2][i // 2].set_title(default_data["ticker"])
    #     axs[i % 2][i // 2].plot(chart_data[0], label="Прогноз")
    #     axs[i % 2][i // 2].plot(chart_data[1], label="Исходные данные")
    #     plt.legend()
    #
    # plt.show()
