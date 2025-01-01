# This code merges tiff files with same extent into one tiff

# Define function to find max reflectance values
import numpy as np


def max_merge_method(old_data, new_data, old_nodata, new_nodata, index=None):
    """
    Custom merge function to take the maximum value where datasets overlap.
    Assumes that the nodata values are marked identically in both datasets.
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

# Open all raster datasets to be merged
folder_path = r"E:\UAH_Classes\Research\Kansas\ECOSTRESS_LST"
file_paths = glob.glob(folder_path + '*.tif')
datasets = [rasterio.open(f) for f in file_paths]

# Use the custom function for merging with the 'max' method
mosaic, out_transform = merge(datasets, method=max_merge_method)

# Example for saving the mosaic to a file
out_meta = datasets[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_transform,
    "count": mosaic.shape[0]
})

with rasterio.open(folder_path + 'Results/mosaic_max.tif', 'w', **out_meta) as out_ds:
    out_ds.write(mosaic)

