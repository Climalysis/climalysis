import xarray as xr
from climalysis.utils import normalize_longitudes
import os

class NinoSSTLoader:
    """
    This class facilitates loading and processing of sea surface temperature (SST) data for different Nino regions, including the computation of Trans-Niño Index (TNI). The Nino regions supported are 1+2, 3, 3.4, 4, ONI, and TNI.

    Upon instantiation, the user provides the path to the SST data file, the desired Nino region, and optionally the start and end times for the period of interest.

    The SST data is loaded from a .nc file using the xarray library. It is then processed according to the latitudes and longitudes corresponding to the specified Nino region.

    Attributes
    ----------
    file_name_and_path : str
        The directory path and file name of the SST data file.
    region : str
        The Nino region for which to load data ('1+2', '3', '3.4', '4', 'ONI', 'TNI').
    start_time : str, optional
        The start of the time slice. Defaults to '1959-01'.
    end_time : str, optional
        The end of the time slice. Defaults to '2022-12'.
    step : int
        The length of the time window (in months) for computing the centered running average. 
        For odd-sized windows, the computed average is placed at the exact center of the window. 
        For even-sized windows, the average is positioned to the right of the center. 
        For example, with a 3-month window, the average of January, February, and March is placed in 
        February; with a 2-month window, the average of January and February is placed in February.

    Methods
    -------
    load_and_process_data():
        Loads the SST data from the .nc file, processes it for the specified Nino region, and returns the processed data as an xarray DataArray.
    
    Index Breakdown
    -------------
    The Nino regions are defined as follows:
    - Niño 1+2: 10°S–0°, 90°W–80°W
    - Niño 3: 5°N-5°S, 150°W-90°W
    - Niño 3.4: 5°N-5°S, 170°W-120°W
    - Niño 4: 5°N-5°S, 160°E-150°W
    - ONI: Same as Niño 3.4, used for Oceanic Niño Index
    - TNI: Computed as the difference in normalized SST anomalies between Niño 1+2 and Niño 4 regions.
    - Custom: Placeholder for user-defined regions.

    References
    ----------
    - Trenberth, K. E., & Stepaniak, D. P. (2001). Indices of El Niño Evolution. Journal of Climate, 14(8), 1697–1701.
    - NOAA Climate Prediction Center: https://www.cpc.ncep.noaa.gov/
    """

    def __init__(self, file_name_and_path, region, start_time='1959-01', end_time='2022-12', step=1, custom_lat_range=None, custom_lon_range=None):
        """
        Initialize NinoSSTLoader with file name, region, time parameters, and step size.

        Parameters:
        ...
        step (int, optional): The length of the time window (in months) for computing the running average. Defaults to 1.
        """
        self.data = file_name_and_path  # can be path string or xr.Dataset
        self.region = region
        self.start_time = start_time
        self.end_time = end_time
        self.step = step
        self.region_dict = {
            '1+2': ((-10, 0), normalize_longitudes((270, 280))),
            '3': ((-5, 5), normalize_longitudes((210, 270))),
            '3.4': ((-5, 5), normalize_longitudes((190, 240))),
            '4': ((-5, 5), normalize_longitudes((200, 210))),
            'ONI': ((-5, 5), normalize_longitudes((190, 240))),
            'TNI': None,
            'Custom': (custom_lat_range, normalize_longitudes(custom_lon_range) if custom_lon_range else None)
        }
        self.lat_range, self.lon_range = self.region_dict[region] if self.region != 'TNI' else (None, None)

        # Validate the information provided
        if not isinstance(file_name_and_path, (str, xr.Dataset)):
            raise ValueError("File must be a string path or an xarray.Dataset.") 
        if not isinstance(region, str):
            raise ValueError("Region must be a string.")
        if not isinstance(start_time, str):
            raise ValueError("Start time must be a string.")
        if not isinstance(end_time, str):
            raise ValueError("End time must be a string.")
        if not isinstance(step, int):
            raise ValueError("Step must be an integer.")
        if step < 1:
            raise ValueError("Step must be a positive integer.")
        if not (start_time <= end_time):
            raise ValueError("Start time must be less than or equal to end time.")
        if region not in self.region_dict:
            raise ValueError("Unsupported region. Supported regions are '1+2', '3', '3.4', '4', 'ONI', 'TNI'.")
        if isinstance(self.data, str):
            if not self.data.endswith('.nc'):
                raise ValueError("The file must be a .nc file.")
            if not os.path.exists(self.data):
                raise FileNotFoundError(f"The file {self.data} does not exist.")

        # Checks for custom lat/lon ranges
        if self.region == 'Custom':
            if self.lat_range is None or self.lon_range is None:
                raise ValueError("For 'Custom' region, you must provide both 'custom_lat_range' and 'custom_lon_range'. These should be tuples of (min, max).")
            if len(self.lat_range) != 2 or len(self.lon_range) != 2:
                raise ValueError("Latitude and longitude ranges must be tuples of length 2: (min, max).")
            if self.lat_range[0] < -90 or self.lat_range[1] > 90:
                raise ValueError("Latitude values must be between -90 and 90.")
            if self.lat_range[0] >= self.lat_range[1]:
                raise ValueError("Latitude range is invalid. The first value must be less than the second.")
            if self.lon_range[0] >= self.lon_range[1]:
                raise ValueError("Longitude range is invalid. The first value must be less than the second.")

    def load_and_process_data(self):
        """
        Loads the SST data from the .nc file, processes it for the specified Nino region, and applies a running average over the defined step size. If the region is 'ONI', the step size is forced to 3 months, regardless of the user-specified step size.

        Returns:
        var_nino (xarray.DataArray): The processed SST data for the specified Nino region.
        """
        # Load the SST data
        var_sst = xr.open_dataset(self.data) if isinstance(self.data, str) else self.data
        var_sst = var_sst.sel(time=slice(self.start_time, self.end_time))
        
        # Normalize longitudes to [-180, 180] if necessary
        var_sst['lon'] = normalize_longitudes(var_sst.lon)
        
        if self.region != 'TNI':
            var_nino = var_sst.sst.where(
                (var_sst.lat <= self.lat_range[1]) & 
                (var_sst.lat >= self.lat_range[0]) & 
                (var_sst.lon <= self.lon_range[1]) & 
                (var_sst.lon >= self.lon_range[0]), drop=True
            )
            var_nino = var_nino.mean(dim=['lon', 'lat'])
        else:
            # For TNI, compute the difference in normalized SST anomalies between the Niño 1+2 and Niño 4 regions.
            lat_range_12, lon_range_12 = self.region_dict['1+2']
            lat_range_4, lon_range_4 = self.region_dict['4']
            var_nino_12 = var_sst.sst.where(
                (var_sst.lat <= lat_range_12[1]) & 
                (var_sst.lat >= lat_range_12[0]) & 
                (var_sst.lon <= lon_range_12[1]) & 
                (var_sst.lon >= lon_range_12[0]), drop=True
            )
            var_nino_12 = var_nino_12.mean(dim=['lon', 'lat'])
            var_nino_4 = var_sst.sst.where(
                (var_sst.lat <= lat_range_4[1]) & 
                (var_sst.lat >= lat_range_4[0]) & 
                (var_sst.lon <= lon_range_4[1]) & 
                (var_sst.lon >= lon_range_4[0]), drop=True
            )
            var_nino_4 = var_nino_4.mean(dim=['lon', 'lat'])
            var_nino = var_nino_12 - var_nino_4
        step = 3 if self.region == 'ONI' else self.step
        var_nino = var_nino.rolling(time=step, center=True).mean()
        return var_nino
