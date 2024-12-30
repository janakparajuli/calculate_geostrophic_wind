# Python code to reproject and extract intersection of shp files
import pandas as pd
import geopandas as gpd
import os

# Read shapefiles
folder = r"E:\UAH_Classes\Research\Kansas"
print(f"Reading files ...")
clip_file = os.path.join(folder, r"PWS\PWSBuffer250.shp")
shp_file = os.path.join(folder, r"Buildings\Heights\glo3DBuildings.shp")

clip_file = gpd.read_file(clip_file)
shp_file = gpd.read_file(shp_file)

# Ensure the CRS matches for all GeoDataFrames before overlay
print("Comparing CRS")
if shp_file.crs != clip_file.crs:
    print("CRS mismatch detected, aligning CRS...")
    shp_file = shp_file.to_crs(clip_file.crs)

else:
    print("CRS matches for both files")

print(clip_file.crs)
print(shp_file.crs)
print("All set for clipping now")

# Intersect both shapefiles
print(f"Intersecting ...")
glo3DBuildings_PWS250 = gpd.overlay(clip_file, shp_file, how = 'intersection', keep_geom_type=False)

print(f"Saving ...")
#glo3DBuildings.to_file(os.path.join(folder, "Buildings","Heights","glo3DBuildings.shp"))
glo3DBuildings_PWS250.to_file(os.path.join(folder, "Buildings","Heights","glo3DBuildings_PWS250.shp"))
print("Operation Completed ...")

