# Python code to extract intersection of shp files
import pandas as pd
import geopandas as gpd
import os

# Read shapefiles
folder = r"E:\UAH_Classes\Research\Kansas"
print(f"Reading files ...")
clip_file = os.path.join(folder, r"Boundary\KansasCity_MO_UA_mer.shp")
shp_file1 = os.path.join(folder, r"Buildings\Heights\3D-GloBFP\United_States_of_America\Kansas.shp")
shp_file2 = os.path.join(folder, r"Buildings\Heights\3D-GloBFP\United_States_of_America\Missouri.shp")

clip_file = gpd.read_file(clip_file)
file1 = gpd.read_file(shp_file1)
file2 = gpd.read_file(shp_file2)

# Merge two shapefiles
print("Merging Files ...")
merged_shp_file = gpd.GeoDataFrame(pd.concat([file1, file2], ignore_index=True))

# Ensure the CRS matches for all GeoDataFrames before overlay
# print("Comparing CRS")
# if merged_shp_file.crs != clip_file.crs:
#     print("CRS mismatch detected, aligning CRS...")
#     merged_shp_gdf = merged_shp_file.to_crs(clip_file.crs)
# print("All set for clipping now")

# Intersect both shapefiles
print(f"Intersecting ...")
# glo3DBuildings = gpd.overlay(clip_file, merged_shp_file, how = 'intersection')

print(f"Saving ...")
#glo3DBuildings.to_file(os.path.join(folder, "Buildings","Heights","glo3DBuildings.shp"))
merged_shp_file.to_file(os.path.join(folder, "Buildings","Heights","KM_glo3DBuildings.shp"))
print("Operation Completed ...")

