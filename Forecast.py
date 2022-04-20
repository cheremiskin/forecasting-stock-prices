import pandas as pd


class ForecastMethodInterface:
    """
    Класс для прогнозирования
    """

    @staticmethod
    def forecast(data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError
