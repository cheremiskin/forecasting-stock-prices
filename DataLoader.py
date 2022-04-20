import time
import yfinance as yf
import pandas as pd
from collections import Callable


class DataLoader:
    def __init__(self, ticker, start_period, end_period, valid_period=5):
        self.end_period = end_period
        self.start_period = start_period
        self.ticker = ticker
        self.stock_data = None
        self.last_load_time = time.time()
        self.update_frequency = valid_period * 60

    def load_data(self):
        self.stock_data = yf.download(self.ticker, self.start_period, self.end_period)

    def data_is_outdated(self):
        return self.last_load_time - time.time() > self.update_frequency

    def get_data(self, data_formatter: Callable[[pd.DataFrame], pd.DataFrame] = None):
        if self.stock_data is None or self.data_is_outdated():
            self.load_data()

        if data_formatter:
            return data_formatter(self.stock_data)
        return self.stock_data
