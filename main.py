import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import MathUtils
from DataLoader import DataLoader
from ForecastingMethods.WalshForecast import WalshForecasting
from GrayCodeBuilder import GrayCodeBuilder


def data_formatter(data: pd.DataFrame):
    data = data.filter(["Adj Close"], axis=1)
    data = data.rename(columns={"Adj Close": "Value"})
    return data


def show_wal():
    T = 1000
    plt.figure(figsize=(14, 7))
    plt.subplots_adjust(wspace=0.35, top=0.94, hspace=0.56)
    t = np.linspace(0, T, 1000)

    for i in range(16):
        w = list(
            map(
                lambda ti: MathUtils.Walsh(
                    i, ti / T, GrayCodeBuilder(math.ceil(math.log2(40)) + 1)
                ),
                t,
            )
        )
        plt.subplot(4, 4, i + 1)
        plt.plot(t, w)
        plt.title("Функция Уолша " + str(i) + " порядка")
        # plt.ylabel("w" + str(i), fontsize=14)  # ось ординат
        plt.grid(True)  # включение отображение сетки

    plt.show()


if __name__ == "__main__":
    default_data = {
        "ticker": "AAPL",
        "start_period": "2019-04-01",
        "end_period": "2021-04-01",
    }

    data_loader = DataLoader(
        ticker=default_data["ticker"],
        start_period=default_data["start_period"],
        end_period=default_data["end_period"],
    )

    # print(MathUtils.Walsh(5, 0.1))

    stock_data: pd.DataFrame = data_loader.get_data(data_formatter=data_formatter)

    plt.plot(stock_data)
    plt.plot(WalshForecasting(stock_data).forecast())

    plt.show()

    # show_wal()
