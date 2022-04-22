import pandas as pd
import matplotlib.pyplot as plt

import MathUtils
from DataLoader import DataLoader
from ForecastingMethods.WalshForecast import WalshForecasting


def data_formatter(data: pd.DataFrame):
    data = data.filter(["Adj Close"], axis=1)
    data = data.rename(columns={"Adj Close": "Value"})
    return data


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
