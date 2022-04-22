import pandas as pd
from abc import ABCMeta, abstractmethod


class ForecastMethodInterface:
    """
    Класс для прогнозирования
    """

    __metaclass__ = ABCMeta

    def __init__(self, data: pd.DataFrame):
        self.data = data

    @abstractmethod
    def forecast(self) -> pd.DataFrame:
        pass