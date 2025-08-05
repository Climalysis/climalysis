# movingAverage.py
import numpy as np

def moving_average(a, n=3, mode='leading', func=np.mean):
    """
    Calculate the moving average of a 1D NumPy array using a specified averaging function and window alignment.

    Supported modes:
    - 'leading':  Average is computed from a[i:i+n] and stored at index i.
    - 'trailing': Average is computed from a[i-n+1:i+1] and stored at index i.
    - 'centered': Average is computed from a[i-k:i+k+1] and stored at index i, where k = n // 2.

    Parameters
    ----------
    a : ndarray
        Input data as a 1D NumPy array. Must not be empty or contain NaN or infinity values.
    n : int, optional
        Window size for the moving average. Must be a positive integer ≤ len(a). Default is 3.
    mode : {'leading', 'trailing', 'centered'}, optional
        Defines where the window is aligned relative to the index. Default is 'leading'.
    func : callable, optional
        Function used to compute the average over each window (e.g., np.mean, np.median). Default is np.mean.

    Returns
    -------
    ndarray
        A NumPy array of the same shape as the input, with NaNs in positions where the moving average
        cannot be computed due to insufficient data.

    Raises
    ------
    ValueError
        If the input is not valid or mode is not recognized.
    """
    if not isinstance(a, np.ndarray) or a.ndim != 1:
        raise ValueError("Input must be a 1-dimensional NumPy array.")
    if len(a) == 0:
        raise ValueError("Input array should not be empty.")
    if np.isnan(a).any():
        raise ValueError("Input array should not contain NaN values.")
    if np.isinf(a).any():
        raise ValueError("Input array should not contain infinity values.")
    if not isinstance(n, int) or n <= 0 or n > len(a):
        raise ValueError("Window size must be a positive integer not exceeding the input length.")
    if mode not in ['leading', 'trailing', 'centered']:
        raise ValueError("Mode must be 'leading', 'trailing', or 'centered'.")

    output = np.full_like(a, np.nan, dtype=float)

    if mode == 'leading':
        for i in range(0, len(a) - n + 1):
            output[i] = func(a[i:i + n])

    elif mode == 'trailing':
        for i in range(n - 1, len(a)):
            output[i] = func(a[i - n + 1:i + 1])

    elif mode == 'centered':
        if n % 2 == 0:
            raise ValueError("Window size must be odd for 'centered' mode.")
        k = n // 2
        for i in range(k, len(a) - k):
            output[i] = func(a[i - k:i + k + 1])

    return output
