import warnings
import statsmodels.api as sm
from statsmodels.tools.sm_exceptions import InterpolationWarning

from StationarityMethods.StationarityMethod import StationarityMethod


class KPSSStationarity(StationarityMethod):
    @staticmethod
    def isStationarity(series: list[float]):
        warnings.simplefilter(action="ignore", category=InterpolationWarning)
        p = sm.tsa.stattools.kpss(series)[1]
        return p > 0.05
