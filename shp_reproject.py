# Python code to extract intersection of shp files
import pandas as pd
import geopandas as gpd
import os

# Read shapefiles
folder = r"E:\UAH_Classes\Research\Kansas"
print(f"Reading files ...")
bound_file = os.path.join(folder, r"Boundary\KansasCity_MO_UA_mer.shp")
shp_file = os.path.join(folder, r"Buildings\Heights\KM_glo3DBuildings.shp")

bound_file = gpd.read_file(bound_file)
shp_file = gpd.read_file(shp_file)

# Ensure the CRS matches for all GeoDataFrames before overlay
print("Comparing CRS")
if shp_file.crs != bound_file.crs:
    print("CRS mismatch detected, aligning CRS...")
    shp_file = shp_file.to_crs(bound_file.crs)

else:
    print("CRS matches for both files")

print(shp_file.crs)
print("All set for clipping now")

# Intersect both shapefiles
# print(f"Intersecting ...")
# # glo3DBuildings = gpd.overlay(clip_file, merged_shp_file, how = 'intersection')

print(f"Saving ...")
#glo3DBuildings.to_file(os.path.join(folder, "Buildings","Heights","glo3DBuildings.shp"))
shp_file.to_file(os.path.join(folder, "Buildings","Heights","KM_glo3DBuildings_Mer.shp"))
print("Operation Completed ...")

