import rasterio
import numpy as np
from scipy.stats import pearsonr
import glob
import os

# Function to read raster data into numpy array with specified bounds
def read_raster_as_array(raster_path, window):
    with rasterio.open(raster_path) as src:
        data = src.read(1, window=window)
        nodata = src.nodata
        # Ensure data is float to handle NaN
        data = data.astype('float32')
        return data, nodata

# Determine the overlapping window based on raster bounds
def get_overlap_window(*rasters):
    min_left = rasters[0].bounds.left
    min_bottom = rasters[0].bounds.bottom
    max_right = rasters[0].bounds.right
    max_top = rasters[0].bounds.top

    for raster in rasters[1:]:
        min_left = max(min_left, raster.bounds.left)
        min_bottom = max(min_bottom, raster.bounds.bottom)
        max_right = min(max_right, raster.bounds.right)
        max_top = min(max_top, raster.bounds.top)

    if min_left >= max_right or min_bottom >= max_top:
        raise ValueError("No overlapping region among the provided rasters.")

    windows = [raster.window(min_left, min_bottom, max_right, max_top) for raster in rasters]
    return windows

# Paths to the raster files
raster_paths = [
    r"E:\UAH_Classes\Research\Kansas\ECOSTRESS_LST\Results\LSTMax10m.tif",
    r"E:\UAH_Classes\Research\Kansas\Buildings\Results\glo3DBld10m_.tif",
    r"E:\UAH_Classes\Research\Kansas\Canopy\kansasCan10m.tif"
]

# Open rasters
rasters = [rasterio.open(path) for path in raster_paths]

try:
    windows = get_overlap_window(*rasters)
except ValueError as e:
    print(e)
    raise SystemExit("Exiting: Raster overlap calculation failed.")

# Read the overlapping part of each raster
raster_data = [read_raster_as_array(raster.name, window) for raster, window in zip(rasters, windows)]

# Stack arrays to a single 3D numpy array (bands, rows, columns)
data_stack = np.stack([data for data, _ in raster_data], axis=0)
nodata_values = [nodata for _, nodata in raster_data]

# Replace nodata with NaN and handle data types
for i, nodata in enumerate(nodata_values):
    if nodata is not None:
        data_stack[i][data_stack[i] == nodata] = np.nan

# Compute pairwise correlation between each pair of rasters
num_rasters = len(raster_paths)
correlation_matrix = np.full((num_rasters, num_rasters), np.nan)

for i in range(num_rasters):
    for j in range(i + 1, num_rasters):
        valid_mask = ~np.isnan(data_stack[i]) & ~np.isnan(data_stack[j])
        if np.any(valid_mask):
            correlation_matrix[i, j], _ = pearsonr(data_stack[i][valid_mask], data_stack[j][valid_mask])
            correlation_matrix[j, i] = correlation_matrix[i, j]

# Close all raster files
for raster in rasters:
    raster.close()

# Print the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)
