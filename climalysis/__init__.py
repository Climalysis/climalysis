from .index.ninoGeneral import NinoSSTLoader
from .index.ECnino import compute_index
from .stats.fisherTransform import FisherTransform
from .stats.linearDetrend import detrend
from .stats.lowessAnalysis import lowessAnalysis
from .stats.movingAverage import moving_average
from .utils.normalizeLongitudes import normalize_longitudes

# Aliases for clean naming
nino_index = NinoSSTLoader
eastern_central_nino_index = compute_index
fisher = FisherTransform
remove_trend = detrend
lowess = lowessAnalysis
rolling_average = moving_average

__all__ = [
    "nino_index",
    "fisher",
    "remove_trend",
    "lowess",
    "rolling_average",
    "normalize_longitudes",
    "eastern_central_nino_index",
]
