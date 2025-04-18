# climalysis/utils/geo.py

import numpy as np
import xarray as xr
from collections.abc import Iterable
import warnings

def normalize_longitudes(lon_values, to="[-180,180]"):
    """
    Normalize longitude values or bounds to a specified range.

    Parameters
    ----------
    lon_values : tuple, list, np.ndarray, or xarray.DataArray
        Input longitude(s) to normalize. Can be:
        - A tuple/list of (min, max)
        - A 1D or multi-dimensional array
        - An xarray.DataArray

    to : str, optional
        Target range for normalization. Must be one of:
        - "[-180,180]" (default)
        - "[0,360]"

    Returns
    -------
    Same type as input (tuple, list, np.ndarray, xarray.DataArray)
        Longitude(s) normalized to the desired range.
        If input is a tuple or list of length 2, the result is ordered (min, max).

    Raises
    ------
    ValueError
        If 'to' is not a supported normalization range.
    TypeError
        If input type is not supported.
    """
    if to not in ["[-180,180]", "[0,360]"]:
        raise ValueError("Supported 'to' values are '[-180,180]' or '[0,360]'.")

    def normalize(val):
        if to == "[-180,180]":
            return ((val + 180) % 360) - 180
        else:
            return val % 360

    # Handle tuple/list input (e.g., bounds)
    if isinstance(lon_values, (tuple, list)):
        normalized = [normalize(lon) for lon in lon_values]

        # If it's a 2-element tuple/list, treat as bounds and enforce (min, max) order
        if len(normalized) == 2:
            lo, hi = normalized
            if lo > hi:
                warnings.warn(
                    f"Longitude bounds reversed to maintain min < max: ({lo}, {hi})",
                    stacklevel=2
                )
                lo, hi = hi, lo
            return type(lon_values)((lo, hi))

        return type(lon_values)(normalized)

    # Handle arrays or DataArrays
    if isinstance(lon_values, (np.ndarray, xr.DataArray)):
        return normalize(lon_values)

    raise TypeError(
        f"Unsupported input type: {type(lon_values)}. "
        "Expected tuple, list, numpy.ndarray, or xarray.DataArray."
    )
