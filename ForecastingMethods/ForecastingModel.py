import pandas as pd
from abc import ABCMeta, abstractmethod


class ForecastingModelInterface:
    __metaclass__ = ABCMeta

    def __init__(self, data: list[float]):
        self.data = data

    @abstractmethod
    def forecast(self, last_values: list[float] = None) -> list[float]:
        pass
