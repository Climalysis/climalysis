
import numpy as np
import numpy.polynomial.polynomial as poly
import pandas as pd
import xarray as xr
from xeofs.single import EOF

def compute_alpha(pc1, pc2):
    coefs = poly.polyfit(pc1, pc2, deg=2)
    xfit = np.arange(pc1.min(), pc1.max() + 0.1, 0.1)
    fit = poly.polyval(xfit, coefs)
    return coefs[-1], xfit, fit

def correction_factor(model):
    _eofs = model.components()
    _subset = dict(lat=slice(-5, 5), lon=slice(140, 180))
    corr_factor = np.zeros(2)
    corr_factor[0] = 1 if _eofs.sel(mode=1, **_subset).mean() > 0 else -1
    corr_factor[1] = 1 if _eofs.sel(mode=2, **_subset).mean() > 0 else -1
    return xr.DataArray(corr_factor, coords=[("mode", [1, 2])])

def compute_index(tos_anom, base_period):
    # select the tropical Pacific region
    tos_anom = tos_anom.sel(lat=slice(-20, 20), lon=slice(100, 280))
    model = EOF(n_modes=2, use_coslat=True)

    # Compute Eofs with the base period
    model.fit(tos_anom.sel(time=slice(*base_period)), dim="time")
    scale_factor = 1 / np.sqrt(model.explained_variance())

    # Compute the correction factor
    corr_factor = correction_factor(model)

    # Project the complete series of anomalies onto the climatological EOFs
    # we apply the scale factor and the correction factor
    pcs = model.transform(tos_anom) * scale_factor * corr_factor

    pc1 = pcs.sel(mode=1)
    pc2 = pcs.sel(mode=2)

    # Perform 45-degree rotation to obtain the E and C indices
    eindex = (pc1 - pc2) / (2 ** (1 / 2))
    eindex.name = "E_index"
    cindex = (pc1 + pc2) / (2 ** (1 / 2))
    cindex.name = "C_index"
    ecindex = xr.merge([eindex, cindex])

    # Select only the winter months (December, January, February)
    # to compute alpha fit
    pc1_djf = pc1.sel(time=pc1.time.dt.month.isin([12, 1, 2]))
    pc1_djf = (
        pc1_djf.resample(time="QS-DEC")
        .mean()
        .dropna("time")
        .sel(time=slice("1980", None))
    )
    pc1_djf["time"] = (
        pc1_djf.indexes["time"].to_series().apply(lambda x: x + pd.DateOffset(years=1))
    )
    pc1_djf.name = "pc1_djf"

    pc2_djf = pc2.sel(time=pc2.time.dt.month.isin([12, 1, 2]))
    pc2_djf = (
        pc2_djf.resample(time="QS-DEC")
        .mean()
        .dropna("time")
        .sel(time=slice("1980", None))
    )
    pc2_djf["time"] = (
        pc2_djf.indexes["time"].to_series().apply(lambda x: x + pd.DateOffset(years=1))
    )
    pc2_djf.name = "pc2_djf"

    pcs_djf = xr.concat([pc1_djf, pc2_djf], dim="mode")

    alpha, xfit, fit = compute_alpha(pc1_djf, pc2_djf)

    return ecindex, pcs, pcs_djf, alpha, xfit, fit