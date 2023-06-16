import numpy as np

def moving_average(a, n=3, fill='filled', position=0):
    """
    Calculate the moving average of a 1D array.

    Parameters
    ----------
    a : ndarray
        Input data as a 1-dimensional numpy array.
    n : int, optional
        Window size for the moving average. Defaults to 3.
    fill : str, optional
        Determines how the output array is filled.
        - 'filled': The output array is filled with NaN values, and the moving average values are inserted at the specified position. (default)
        - 'unfilled': The output array only contains the moving average values.
    position : int, optional
        The position in the output array where the moving average values are inserted. Defaults to 0 (the first spot).

    Returns
    -------
    ndarray
        Array with the moving average values inserted at the specified position (or at the beginning if fill='unfilled').

    Raises
    ------
    ValueError
        If the input 'a' is not a 1-dimensional numpy array or 'n' is not a positive integer,
        or 'fill' parameter is invalid.

    """
    if not isinstance(a, np.ndarray) or a.ndim != 1:
        raise ValueError("Input 'a' must be a 1-dimensional numpy array.")
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Window size 'n' must be a positive integer.")
    if fill not in ['filled', 'unfilled']:
        raise ValueError("Invalid value for 'fill'. Must be 'filled' or 'unfilled'.")

    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    var = ret[n - 1:] / n

    if fill == 'unfilled':
        return var

    output = np.empty_like(a)
    output.fill(np.nan)
    output[position:position + len(var)] = var
    return output
