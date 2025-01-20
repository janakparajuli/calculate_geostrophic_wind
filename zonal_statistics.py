import geopandas as gpd
import rasterio
from rasterio.features import rasterize
import numpy as np
from rasterstats import zonal_stats

# Paths to your data
raster_path = r"E:\UAH_Classes\AES_515\Analysis\lst_web_mer"
shapefile_path = r"E:\UAH_Classes\AES_515\Analysis\KC_Counties.shp"
output_raster_path = r'E:\UAH_Classes\AES_515\Analysis\lst_cnts_mean.tif'

# Load the shapefile
counties = gpd.read_file(shapefile_path)
# Check and set the CRS for the shapefile
if counties.crs is None:
    print("Shapefile has no CRS. Setting to WGS 1984 Web Mercator (EPSG:3857).")
    counties.set_crs("epsg:3857", inplace=True)
elif counties.crs.to_string() != 'epsg:3857':
    print("Reprojecting shapefile to WGS 1984 Web Mercator (EPSG:3857).")
    counties = counties.to_crs(epsg=3857)
else:
    print("Shapefile is already in WGS 1984 Web Mercator (EPSG:3857).")

# Load the raster file
with rasterio.open(raster_path) as src:
    if src.crs is None:
        print("Raster has no CRS. Cannot check projection accurately.")
        raise ValueError("Raster CRS is undefined. Please define or reproject the raster.")
    elif src.crs.to_string() != 'epsg:3857':
        print("Raster is not in the correct projection. Please reproject to WGS 1984 Web Mercator (EPSG:3857).")
        raise ValueError("Incorrect raster CRS. Reprojection needed.")
    else:
        print("Raster is in WGS 1984 Web Mercator (EPSG:3857).")

        # Calculate zonal statistics
        stats = zonal_stats(counties, src.read(1), affine=src.transform, stats="mean", nodata=src.nodata)

        # Add mean temperature to the GeoDataFrame
        counties['mean_temp'] = [stat['mean'] for stat in stats]

        # Create a raster of mean temperatures per county
        mean_temp_map = rasterize(
            [(geom, value) for geom, value in zip(counties.geometry, counties['mean_temp'])],
            out_shape=(src.height, src.width),
            fill=np.nan,  # Fill value outside of counties
            transform=src.transform,
            all_touched=True  # Include all pixels that touch a geometry
        )

        # Update meta to reflect the new single band and data type
        meta.update(dtype=rasterio.float32, count=1, nodata=np.nan)

        # Write out the new raster
        with rasterio.open(output_raster_path, 'w', **meta) as out_raster:
            out_raster.write(mean_temp_map, 1)