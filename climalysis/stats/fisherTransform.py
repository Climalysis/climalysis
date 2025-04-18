#fisherTransform.py
import numpy as np
import math

class FisherTransform:
    """
    A class used to perform Fisher's Z-Transformation on correlation coefficients.

    Methods
    -------
    r_to_Z(r)
        Converts a correlation coefficient to a Fisher Z score.
    Fishers_z_Transform(z1, z2, n1, n2)
        Applies Fisher's Z-Transformation to two Z scores with their corresponding sample sizes.
    standardError_z(n)
        Calculates the standard error of a Z score.
    Fishers_confidence_interval(r, n, confidence)
        Calculates the confidence interval for a correlation coefficient.
        
    References
    ----------
    Devore, J. L.: Probability and Statistics for Engineering and the Sciences, 
    Biometrics, 47, 1638–1638, https://doi.org/10.2307/2532427, 1991.

    Simpson, I. R. and Polvani, L. M.: Revisiting the relationship between jet 
    position, forced response, and annular mode variability in the southern midlatitudes, 
    Geophys. Res. Lett., 43, 2896–2903, https://doi.org/10.1002/2016GL067989, 2016.

    Casselman, J. W., Jiménez-Esteve, B., and Domeisen, D. I. V.: Modulation of the El Niño 
    teleconnection to the North Atlantic by the tropical North Atlantic during boreal spring and summer, 
    Weather Clim. Dynam., 3, 1077–1096, https://doi.org/10.5194/wcd-3-1077-2022, 2022.
    """

    def r_to_Z(self, r):
        """
        Converts a correlation coefficient to a Fisher Z score.
        """
        if not isinstance(r, (int, float)) or r <= -1 or r >= 1:
            raise ValueError("Input 'r' must be a number in the range -1 < r < 1.")
        Z = 0.5 * (np.log(1 + r) - np.log(1 - r))
        return Z

    def Fishers_z_Transform(self, z1, z2, n1, n2):
        """
        Applies Fisher's Z-Transformation to two Z scores with their corresponding sample sizes.
        """
        if not all(isinstance(z, (int, float)) for z in [z1, z2]) or not all(isinstance(n, int) and n > 3 for n in [n1, n2]):
            raise ValueError("Inputs 'z1' and 'z2' must be numbers, and 'n1' and 'n2' must be integers greater than 3.")
        z = (z1 - z2) / np.sqrt(1 / (n1 - 3) + 1 / (n2 - 3))
        return z

    def standardError_z(self, n):
        """
        Calculates the standard error of a Z score.
        """
        if not isinstance(n, int) or n <= 3:
            raise ValueError("Input 'n' must be an integer greater than 3.")
        stderr = 1 / np.sqrt(n - 3)
        return stderr

    def Fishers_confidence_interval(self, r, n, confidence=95):
        """
        Calculates the confidence interval for a correlation coefficient.
        """
        if not isinstance(r, (int, float)) or r <= -1 or r >= 1 or not isinstance(n, int) or n <= 3:
            raise ValueError("Input 'r' must be a number in the range -1 < r < 1, and 'n' must be an integer greater than 3.")
        cf_dict = {90: 1.645, 95: 1.960}
        if confidence not in cf_dict:
            raise ValueError("Unsupported confidence level. Supported levels are 90 and 95.")
        cf = cf_dict[confidence]
        Z = self.r_to_Z(r)
        L = Z - cf / np.sqrt(n - 3)
        U = Z + cf / np.sqrt(n - 3)
        conf_lower = (np.exp(2 * L) - 1) / (np.exp(2 * L) + 1)
        conf_upper = (np.exp(2 * U) - 1) / (np.exp(2 * U) + 1)
        return (conf_lower, conf_upper)
