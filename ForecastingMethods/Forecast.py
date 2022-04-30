import pandas as pd
from abc import ABCMeta, abstractmethod


class ForecastMethodInterface:
    __metaclass__ = ABCMeta

    def __init__(self, data: list[float]):
        self.data = data

    @abstractmethod
    def forecast(self) -> list[float]:
        pass
