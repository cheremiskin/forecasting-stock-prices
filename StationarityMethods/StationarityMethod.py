from abc import ABCMeta, abstractmethod


class StationarityMethod:
    __metaclass__ = ABCMeta

    def __init__(self, data: list[float]):
        self.data = data

    @staticmethod
    @abstractmethod
    def isStationarity(series: list[float]) -> bool:
        pass
