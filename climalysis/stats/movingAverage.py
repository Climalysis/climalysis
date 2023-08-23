import numpy as np

def moving_average(a, n=3, fill='filled', position=0, func=np.mean):
    """
    Calculate the moving average of a 1D array using a specified averaging function.

    Parameters
    ----------
    a : ndarray
        Input data as a 1-dimensional numpy array. Should not be empty or contain NaN or infinity values.
    n : int, optional
        Window size for the moving average. Defaults to 3. Must be a positive integer and cannot exceed the size of the input array.
    fill : str, optional
        Determines how the output array is filled.
        - 'filled': The output array is filled with NaN values, and the moving average values are inserted at the specified position. (default)
        - 'unfilled': The output array only contains the moving average values. The window size and position should not exceed the size of the input array.
    position : int, optional
        The position in the output array where the moving average values are inserted. Defaults to 0 (the first spot). Must be a non-negative integer and cannot exceed the size of the input array.
    func : function, optional
        The function used to calculate the average. Defaults to numpy.mean. 

    Returns
    -------
    ndarray
        Array with the moving average values inserted at the specified position (or at the beginning if fill='unfilled').

    Raises
    ------
    ValueError
        If the input 'a' is not a 1-dimensional numpy array, is empty, or contains NaN or infinity values,
        or 'n' is not a positive integer or exceeds the size of the input array,
        or 'position' is not a non-negative integer or exceeds the size of the input array,
        or 'fill' is not 'filled' or 'unfilled',
        or the combination of 'n' and 'position' would exceed the size of the input array when 'fill' is 'filled'.
    """
    if not isinstance(a, np.ndarray) or a.ndim != 1:
        raise ValueError("Input must be a 1-dimensional numpy array.")
    if np.isnan(a).any():
        raise ValueError("Input array should not contain NaN values.")
    if np.isinf(a).any():
        raise ValueError("Input array should not contain infinity values.")
    if len(a) == 0:
        raise ValueError("Input array should not be empty.")
    if not isinstance(n, int) or n <= 0 or n > len(a):
        raise ValueError("Window size must be a positive integer and cannot exceed the size of the input array.")
    if not isinstance(position, int) or position < 0 or position >= len(a):
        raise ValueError("Position must be a non-negative integer and cannot exceed the size of the input array.")
    if fill not in ['filled', 'unfilled']:
        raise ValueError("Invalid value for 'fill'. Must be 'filled' or 'unfilled'.")
    if fill == 'filled' and position + n > len(a):
        raise ValueError("For 'filled' option, the combination of window size 'n' and position should not exceed the size of the input array.")

    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    var = ret[n - 1:] / n

    if fill == 'unfilled':
        return var

    output = np.empty_like(a)
    output.fill(np.nan)
    output[position:position + n] = func(a[position:position + n])
    return output
