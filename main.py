import pandas as pd
import matplotlib.pyplot as plt

from DataLoader import DataLoader
from ForecastingMethods.MarkovChain import MarkovChain
from PerformanceEvaluationForecastingModel import PerformanceEvaluationForecastingModel


def data_formatter(data: pd.DataFrame):
    data = data.filter(["Adj Close"], axis=1)
    data = data.rename(columns={"Adj Close": "Value"})
    data["Date"] = data.index
    return data


if __name__ == "__main__":
    default_data = {
        "ticker": "T",
        "start_period": "2000-04-01",
        # "start_period": "2020-04-01",
        "end_period": "2021-03-01",
    }

    data_loader = DataLoader(
        ticker=default_data["ticker"],
        start_period=default_data["start_period"],
        end_period=default_data["end_period"],
    )

    stock_data: pd.DataFrame = data_loader.get_data(data_formatter=data_formatter)

    PerformanceEvaluationForecastingModel(
        model=MarkovChain, data=stock_data["Value"].tolist()
    )

    # plt.grid()
    #
    # plt.plot(stock_data["Value"].tolist(), label="Original")
    # plt.plot(
    #     MarkovChain(stock_data["Value"][:-10].tolist()).forecast(),
    #     label="Forecast",
    # )
    # plt.legend()
    #
    # plt.show()
