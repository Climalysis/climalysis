#linearDetrend.py
import numpy as np

def detrend(data):
    """
    Detrend the data by fitting a polynomial and subtracting the trend.

    Parameters
    ----------
    data : array_like
        Input data as a 1-dimensional array or list. Should not be empty or contain NaN or infinity values.

    Returns
    -------
    ndarray
        Detrended data.

    Raises
    ------
    ValueError
        If the input 'data' is not a list-like structure, is empty, is not 1-dimensional,
        contains NaN or infinity values, or has less than two elements (which is insufficient to fit a polynomial).
    """
    # Validation checks
    try:
        data = np.asarray(data)
    except TypeError:
        raise ValueError("Input 'data' must be a list-like structure that can be converted to a numpy array.")
    if not isinstance(data, np.ndarray) or data.ndim != 1:
        raise ValueError("Input 'data' must be a 1-dimensional array or list.")
    if np.isnan(data).any():
        raise ValueError("Input data should not contain NaN values.")
    if np.isinf(data).any():
        raise ValueError("Input data should not contain infinity values.")
    if len(data) == 0:
        raise ValueError("Input data should not be empty.")
    if len(data) < 2:
        raise ValueError("Input data should have at least two elements to fit a polynomial.")

    # Polynomial fitting and detrending
    x = np.arange(len(data))
    z = np.polyfit(x, data, min(1, len(data) - 1))
    yTrend = np.polyval(z, x)
    dataDetrend = data - yTrend
    return dataDetrend
