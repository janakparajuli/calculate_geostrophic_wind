import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from rasterstats import zonal_stats
import numpy as np

# Paths to your data
raster_path = r"E:\UAH_Classes\AES_515\Asignment_1\Dataset\LST\ECO2LSTE.001_SDS_LST_doy2023231183936_aid0001.tif"
# raster_path = r"E:\UAH_Classes\AES_515\Analysis\ECO2LSTE.001_SDS_LST_doy2023231183936_aid0001.tif"
shapefile_path = r"E:\UAH_Classes\AES_515\Analysis\KC_Tracts.shp"
output_raster_path = r'E:\UAH_Classes\AES_515\Analysis\lst_trct_mean.tif'

# Load the shapefile
counties = gpd.read_file(shapefile_path)
if counties.crs is None or not counties.crs.to_string().lower().startswith('epsg'):
    counties.set_crs('epsg:4326', inplace=True)
elif counties.crs.to_string() != 'epsg:4326':
    counties = counties.to_crs('epsg:4326')
counties = counties[counties.geometry.notnull() & counties.is_valid]

# Open the raster file
with rasterio.open(raster_path) as src:
    if src.crs is None or src.crs.to_string() != 'epsg:3857':
        print("Raster CRS is not set or incorrect. Setting to EPSG:3857.")
        src._crs = rasterio.crs.CRS.from_epsg(4326)

    print('crs set')
    if counties.crs != src.crs:
        counties = counties.to_crs(src.crs)

    stats = zonal_stats(counties, src.read(1), affine=src.transform, stats="mean", nodata=src.nodata, all_touched=True)
    counties['mean_temp'] = [stat['mean'] if stat is not None else np.nan for stat in stats]
    print('here')
    mean_temp_map = rasterize(
        [(geom, value) for geom, value in zip(counties.geometry, counties['mean_temp'])],
        out_shape=(src.height, src.width),
        fill=np.nan,
        transform=src.transform,
        all_touched=True
    )

    # Set up metadata for writing
    meta = src.meta.copy()
    meta.update({
        'driver': 'GTiff',  # Specify the GeoTIFF driver
        'dtype': 'float16',
        'count': 1,
        'nodata': np.nan
    })

    # Write out the new raster
    with rasterio.open(output_raster_path, 'w', **meta) as out_raster:
        out_raster.write(mean_temp_map, 1)
