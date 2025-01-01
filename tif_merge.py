import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
import glob
import os

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

# Define the path and find all TIFF files
folder_path = r"E:\UAH_Classes\Research\Kansas\ECOSTRESS_LST"
file_paths = glob.glob(os.path.join(folder_path, '*.tif'))
datasets = [rasterio.open(f) for f in file_paths if f.endswith('.tif')]  # Ensure these are TIFF files

# Check for empty dataset list
if not datasets:
    raise RuntimeError("No TIFF files found in the specified directory.")

# Merge using the custom max function
mosaic, out_transform = merge(datasets, method=max_merge_method)

# Desired CRS and resolution
desired_crs = 'EPSG:3857'
desired_resolution = 10

# Get transformation and metadata for reprojecting
transform, width, height = calculate_default_transform(
    datasets[0].crs, desired_crs, datasets[0].width, datasets[0].height, *datasets[0].bounds, resolution=desired_resolution)

out_meta = datasets[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": height,
    "width": width,
    "transform": transform,
    "crs": desired_crs,
    "count": mosaic.shape[0]
})

# Reproject and resample the mosaic to desired CRS and resolution
reprojected_mosaic = np.zeros((mosaic.shape[0], height, width), dtype=mosaic.dtype)
for i in range(mosaic.shape[0]):  # For each band
    reproject(
        mosaic[i],
        reprojected_mosaic[i],
        src_transform=out_transform,
        src_crs=datasets[0].crs,
        dst_transform=transform,
        dst_crs=desired_crs,
        resampling=Resampling.bilinear  # Using bilinear resampling for continuous data
    )

# Save the reprojected and resampled mosaic to file
output_file = os.path.join(folder_path, 'Results', 'mosaic_max_3857_10m.tif')
with rasterio.open(output_file, 'w', **out_meta) as out_ds:
    out_ds.write(reprojected_mosaic)
