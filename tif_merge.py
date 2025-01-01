import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
import glob
import os

def max_merge_method(old_data, new_data, old_nodata, new_nodata, index=None, **kwargs):
    # Custom merge function as before
    mask = (old_data != old_nodata) & (new_data != new_nodata)
    return np.where(mask, np.maximum(old_data, new_data), old_data)

folder_path = r"E:\UAH_Classes\Research\Kansas\ECOSTRESS_LST"
file_paths = glob.glob(os.path.join(folder_path, '*.tif'))
datasets = [rasterio.open(f) for f in file_paths if f.endswith('.tif')]

if not datasets:
    raise RuntimeError("No TIFF files found in the specified directory.")

# Merge datasets
mosaic, out_transform = merge(datasets, method=max_merge_method)
nodata = datasets[0].nodata  # Assuming all datasets have the same nodata value

# Desired CRS, resolution, and metadata for output
desired_crs = 'EPSG:3857'
desired_resolution = 10
out_meta = datasets[0].meta.copy()
transform, width, height = calculate_default_transform(
    datasets[0].crs, desired_crs, datasets[0].width, datasets[0].height, *datasets[0].bounds, resolution=desired_resolution)
out_meta.update({
    "driver": "GTiff",
    "height": height,
    "width": width,
    "transform": transform,
    "crs": desired_crs,
    "nodata": nodata,
    "dtype": 'float32'  # Ensure correct data type if needed
})

# Reproject and resample the mosaic
reprojected_mosaic = np.full((mosaic.shape[0], height, width), nodata, dtype='float32')  # Initialize with nodata
for i in range(mosaic.shape[0]):  # For each band
    reproject(
        source=mosaic[i],
        destination=reprojected_mosaic[i],
        src_transform=out_transform,
        src_crs=datasets[0].crs,
        dst_transform=transform,
        dst_crs=desired_crs,
        src_nodata=nodata,
        dst_nodata=nodata,
        resampling=Resampling.nearest  # Change to nearest if appropriate
    )

output_file = os.path.join(folder_path, 'Results', 'mosaic_max_3857_10m.tif')
with rasterio.open(output_file, 'w', **out_meta) as out_ds:
    out_ds.write(reprojected_mosaic)

print("Completed Operation ... ")