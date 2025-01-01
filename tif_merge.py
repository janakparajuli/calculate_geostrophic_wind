import numpy as np
import rasterio
from rasterio.merge import merge  # Corrected import statement for merge
from rasterio.warp import reproject, Resampling, calculate_default_transform
import glob
import os

# Load datasets
folder_path = r"E:\UAH_Classes\Research\Kansas\ECOSTRESS_LST"
file_paths = glob.glob(os.path.join(folder_path, '*.tif'))
if not file_paths:
    raise RuntimeError("No files found. Check the path.")

datasets = [rasterio.open(f) for f in file_paths]
if not datasets:
    raise RuntimeError("Failed to open files.")

# Merge datasets using the maximum value method
mosaic, out_transform = merge(datasets, method='max')  # Use of the corrected merge function

# Set destination CRS and calculate transformation
dest_crs = 'EPSG:3857'
transform, width, height = calculate_default_transform(
    datasets[0].crs, dest_crs, datasets[0].width, datasets[0].height,
    *datasets[0].bounds, resolution=10)

# Prepare output metadata
out_meta = datasets[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": height,
    "width": width,
    "transform": transform,
    "crs": dest_crs,
    "dtype": rasterio.float32
})

# Reproject and resample
reprojected = np.full((mosaic.shape[0], height, width), out_meta['nodata'], dtype=rasterio.float32)
for i in range(mosaic.shape[0]):
    reproject(
        source=mosaic[i],
        destination=reprojected[i],
        src_transform=out_transform,
        dst_transform=transform,
        src_crs=datasets[0].crs,
        dst_crs=dest_crs,
        src_nodata=datasets[0].nodata,
        dst_nodata=out_meta['nodata'],
        resampling=Resampling.bilinear
    )

# Output the result
output_path = os.path.join(folder_path, 'Results', 'mosaic_max_3857_10m.tif')
with rasterio.open(output_path, 'w', **out_meta) as dst:
    dst.write(reprojected)
    dst.build_overviews([2, 4, 8, 16, 32], Resampling.nearest)
    dst.update_tags(ns='rio_overview', resampling='nearest')

# Ensure the file has statistics
with rasterio.open(output_path) as src:
    for band in range(1, src.count + 1):
        data = src.read(band)
        if np.all(data == src.nodata):
            print(f"No valid data in band {band}")
        else:
            print(f"Statistics for band {band}: min={data.min()}, max={data.max()}, mean={data.mean()}")
