import numpy as np

def max_merge_method(old_data, new_data, old_nodata, new_nodata, index=None, **kwargs):
    """
    Custom merge function to take the maximum value where datasets overlap.
    Assumes that the nodata values are marked identically in both datasets.
    Accepts arbitrary keyword arguments (**kwargs) to be compatible with rasterio's internal calls.
    """
    # Create a mask where either the old data or new data is not nodata
    mask = (old_data != old_nodata) & (new_data != new_nodata)

    # Use maximum value from old and new data where mask is True
    max_data = np.maximum(old_data, new_data)

    # Where the mask is False, keep the old data values (preserve existing data)
    return np.where(mask, max_data, old_data)

import rasterio
from rasterio.merge import merge
import glob
import os

# Define the path and find all TIFF files
folder_path = r"E:\UAH_Classes\Research\Kansas\ECOSTRESS_LST"
file_paths = glob.glob(os.path.join(folder_path, '*.tif'))
datasets = [rasterio.open(f) for f in file_paths if f.endswith('.tif')]  # Ensure these are TIFF files

# Check for empty dataset list
if not datasets:
    raise RuntimeError("No TIFF files found in the specified directory.")

# Merge using the custom max function
mosaic, out_transform = merge(datasets, method=max_merge_method)

# Metadata for output
out_meta = datasets[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_transform,
    "count": mosaic.shape[0]
})

# Save the merged mosaic to file
output_file = os.path.join(folder_path, 'Results', 'mosaic_max.tif')
with rasterio.open(output_file, 'w', **out_meta) as out_ds:
    out_ds.write(mosaic)
