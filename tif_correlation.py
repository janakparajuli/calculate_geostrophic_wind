import rasterio
import numpy as np
from scipy.stats import pearsonr
import os

# Function to read raster data into numpy array
def read_raster_as_array(raster_path):
    with rasterio.open(raster_path) as src:
        return src.read(1), src.nodata  # Reading the first band and nodata value

# Paths to the raster files
raster_paths = [
    r"E:\UAH_Classes\Research\Kansas\ECOSTRESS_LST\Results\LSTMax10m.tif",
    r"E:\UAH_Classes\Research\Kansas\Buildings\Results\glo3DBld10m_.tif",
    r"E:\UAH_Classes\Research\Kansas\Canopy\kansasCan10m.tif"
]

# Read all rasters into arrays
rasters = [read_raster_as_array(path) for path in raster_paths]

# Check if all rasters have the same shape
if not all(r.shape == rasters[0][0].shape for r, _ in rasters):
    raise ValueError("All rasters must have the same dimensions and resolution.")

# Stack arrays to a single 3D numpy array (bands, rows, columns)
data_stack = np.stack([r for r, nodata in rasters], axis=0)
nodata_values = [nodata for _, nodata in rasters]

# Mask out nodata values, replace them with NaN for correlation computation
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

# Print the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)

# Optionally, handle the output of correlation values
# You can save this matrix or process it further as needed
