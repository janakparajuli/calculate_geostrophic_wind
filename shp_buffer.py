# Computes buffer of a shapefile

import geopandas as gpd
import os

# Path to the input point shapefile
folder = r"E:\UAH_Classes\Research\Kansas"  # Replace with your directory path
filename = "\PWS\kansasPWS.shp"  # Replace with your shapefile name
input_path = os.path.join(folder, filename)

# Path to the output buffer shapefile
output_filename = "PWSBuffer250.shp"
output_path = os.path.join(folder, "PWS", output_filename)

# Read the point shapefile
print("File Reading...")
points_gdf = gpd.read_file(input_path)

# Specify the buffer distance in the units of the shapefile's coordinate system
buffer_distance = 250  # Change this value based on your specific requirements

# Create a buffer around each point
points_gdf['geometry'] = points_gdf.buffer(buffer_distance)

# Save the buffered geometry to a new shapefile
points_gdf.to_file(output_path)

print(f"Buffered shapefile saved to: {output_path}")
