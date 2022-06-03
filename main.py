import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

from DataLoader import DataLoader
from ForecastingMethods.ARIMA import BoxJenkinsMethod, ARIMA
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


if __name__ == "__main__":
    default_data = {
        "ticker": "F",
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
    stock_data_list = stock_data["Value"].tolist()

    min_mse = 2000000000

    pp = -1
    qq = -1

    forecast = []

    train_data = stock_data_list[: round(len(stock_data_list) * 0.9)]
    test_data = stock_data_list[len(train_data) :]

    for p in range(5):
        for q in range(5):
            print("p:", p, ", q:", q)
            if p < 1 or q < 1:
                continue
            train_data = stock_data_list[: round(len(stock_data_list) * 0.9)]
            test_data = stock_data_list[len(train_data) :]

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

    print(min_mse, pp, qq)

    # Plot().plot(stock_data_list)
    # Plot().plot(train_data)
    #
    # Plot().show()

    plt.plot(test_data)
    plt.plot(forecast)

    # print(lag_data(_data, 2))
    # print(_data)

    # bj = BoxJenkinsMethod(stock_data["Value"].tolist())
    # print(bj.calculate_d())

    # PerformanceEvaluationForecastingModel(
    #     model=MarkovChain, data=stock_data["Value"].tolist()
    # )

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
