import xarray as xr
from climalysis import nino_index

def test_nino_index_output_shape():
    # Use a small dummy NetCDF file for testing
    test_file = "tests/data/sst.mon.ltm.1981-2010.nc"
    
    result = nino_index(test_file, region="3.4").load_and_process_data()
    
    assert isinstance(result, xr.DataArray)
    assert "time" in result.dims
    assert result.size > 0  # Basic check to ensure data loaded
