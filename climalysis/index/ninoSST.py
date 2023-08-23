import xarray as xr

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
    """
    def __init__(self, file_name_and_path, region, start_time='1959-01', end_time='2022-12', step=1):
        """
        Initialize NinoSSTLoader with file name, region, time parameters, and step size.

        Parameters:
        ...
        step (int, optional): The length of the time window (in months) for computing the running average. Defaults to 1.
        """
        self.file_name = file_name_and_path
        self.region = region
        self.start_time = start_time
        self.end_time = end_time
        self.step = step
        self.region_dict = {
            '1+2': ((0, 10), (270, 280)),
            '3': ((-5, 5), (210, 270)),
            '3.4': ((-5, 5), (190, 240)),
            '4': ((-5, 5), (200, 210)),
            'ONI': ((-5, 5), (190, 240)), # Same as Nino 3.4
            'TNI': None  # Requires separate computation
        }
        if region not in self.region_dict:
            raise ValueError("Unsupported region. Supported regions are '1+2', '3', '3.4', '4', 'ONI', 'TNI'.")
        self.region = region
        self.lat_range, self.lon_range = self.region_dict[region] if self.region != 'TNI' else (None, None)

    def load_and_process_data(self):
        """
        Loads the SST data from the .nc file, processes it for the specified Nino region, and applies a running average over the defined step size. If the region is 'ONI', the step size is forced to 3 months, regardless of the user-specified step size.

        Returns:
        var_nino (xarray.DataArray): The processed SST data for the specified Nino region.
        """
        var_sst = xr.open_dataset(self.file_name)
        var_sst = var_sst.sel(time=slice(self.start_time, self.end_time))
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
