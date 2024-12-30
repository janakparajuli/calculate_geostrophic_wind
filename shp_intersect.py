# Python code to extract intersection of shp files
import geopandas as gpd
import os

# Read shapefiles
folder = r"E:\UAH_Classes\Research\Kansas\"
clip_file = os.path.join(folder + r"Boundary\KansasCity_MO_UA_mer.shp")
shp_file1 = os.path.join(folder + r"Buildings\Heights\3D-GloBFP\United_States_of_America\Kansas.shp")
shp_file2 = os.path.join(folder + r"Buildings\Heights\3D-GloBFP\United_States_of_America\Missouri.shp")

# Intersect three shapefiles
glo3DBuildings = gpd.overlay(clip_file, shp_file1, shp_file2, how = 'intersection')

glo3DBuildings.to_file(os.path.join(folder + r"Buildings\Heights\glo3DBuildings.shp"))


