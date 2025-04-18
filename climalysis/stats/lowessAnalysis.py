#linearDetrend.py
import numpy as np
import scipy.interpolate
import scipy.stats
from sklearn.metrics import mean_squared_error
from statsmodels.nonparametric.smoothers_lowess import lowess as sm_lowess
import statsmodels.api as sm

class lowessAnalysis:
    """
    This class contains methods for calculating lowess curves, bootstrapping and linear fitting.

    Attributes
    ----------
    x : ndarray
        1D numpy array of x values.
    y : ndarray
        1D numpy array of y values.
    xgrid : ndarray
        1D numpy array of evenly spaced numbers over the range of x values.
    """

    def __init__(self, x, y):
        """
        Constructs all the necessary attributes for the lowessAnalysis object.

        Parameters
        ----------
        x : array-like
            X-axis data.
        y : array-like
            Y-axis data.
        """
        try:
            self.x = np.asarray(x)
            self.y = np.asarray(y)
        except TypeError:
            raise ValueError("Inputs 'x' and 'y' must be list-like structures that can be converted to numpy arrays.")

        if not isinstance(self.x, np.ndarray) or self.x.ndim != 1:
            raise ValueError("Input 'x' must be a 1-dimensional array or list.")
        if not isinstance(self.y, np.ndarray) or self.y.ndim != 1:
            raise ValueError("Input 'y' must be a 1-dimensional array or list.")
        if np.isnan(self.x).any() or np.isnan(self.y).any():
            raise ValueError("Input data should not contain NaN values.")
        if np.isinf(self.x).any() or np.isinf(self.y).any():
            raise ValueError("Input data should not contain infinity values.")
        if len(self.x) != len(self.y):
            raise ValueError("Inputs 'x' and 'y' should have the same length.")

        self.xgrid = np.linspace(self.x.min(), self.x.max())

    def lowess_single(self):
        """
        Creates a single LOWESS (Locally Weighted Scatterplot Smoothing) curve using bootstrapped samples.

        Returns
        -------
        ndarray
            Interpolated y values for the LOWESS curve.
        """
        samples = np.random.choice(len(self.x), len(self.x), replace=True)
        x_s = self.x[samples]
        y_s = self.y[samples]
        y_sm = sm_lowess(y_s, x_s, frac=1./5., it=5, return_sorted=False)
        y_grid = scipy.interpolate.interp1d(x_s, y_sm, fill_value='extrapolate')(self.xgrid)
        return y_grid

    def lowess_bootstrap(self, K=1000):
        """
        Bootstrap method to calculate the mean and standard error of the LOWESS curves.

        Parameters
        ----------
        K : int, optional
            Number of bootstrap samples. Defaults to 1000.

        Returns
        -------
        ndarray
            Mean of the bootstrapped LOWESS curves.
        ndarray
            Standard error of the bootstrapped LOWESS curves.
        """
        if not isinstance(K, int) or K <= 0:
            raise ValueError("Steps 'K' must be a positive integer.")
        smooths = [self.lowess_single() for _ in range(K)]
        smooths = np.array(smooths).T
        mean = np.nanmean(smooths, axis=1)
        stderr = scipy.stats.sem(smooths, axis=1)
        stderr = np.nanstd(smooths, axis=1, ddof=0)
        return mean, stderr

    def return_lowess_boot(self, K=1000):
        """
        Returns the mean, standard error, and x values of the bootstrapped LOWESS curves.

        Parameters
        ----------
        K : int, optional
            Number of bootstrap samples. Defaults to 1000.

        Returns
        -------
        tuple
            Mean of the bootstrapped LOWESS curves.
            Standard error of the bootstrapped LOWESS curves.
            X values.
        """
        mean, stderr = self.lowess_bootstrap(K=K)
        if len(mean) == 0 or len(stderr) == 0:
            raise ValueError("Bootstrap result is empty.")
        return mean, stderr, self.xgrid

    def linearFit(self):
        """
        Performs linear regression on the x and y data, and calculates the root mean square error (RMSE) of the fit.

        Returns
        -------
        tuple
            X values.
            Predicted y values from linear regression.
            RMSE of the fit.
        """
        x_full = self.x.copy()
        y_full = self.y.copy()
        idx = np.isfinite(x_full) & np.isfinite(y_full)
        x_full = x_full[idx].reshape(-1, 1)
        y_full = y_full[idx].reshape(-1, 1)
        #-------------------- Preform Analysis:--------------------------------------#
        X2 = sm.add_constant(x_full)
        model = sm.OLS(y_full, X2).fit()
        ypred = model.predict(X2)
        pvalues = model.pvalues[1]
        RMSEstorage = np.sqrt(mean_squared_error(y_full, ypred))

        return x_full,ypred,RMSEstorage