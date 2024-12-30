# Computes buffer of a shapefile

import geopandas as gpd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Path to the input point shapefile
folder = r"E:\UAH_Classes\Research\Kansas"  # Replace with your directory path
filename = r"PWS\kansasPWS.shp"  # Replace with your shapefile name
input_path = os.path.join(folder, filename)

# Path to the output buffer shapefile
buffer_distance = 20  # Value changes based on requirements

output_filename = f"PWSBuffer{buffer_distance}.shp"
output_path = os.path.join(folder, "PWS", output_filename)
print(output_filename)

# Read the point shapefile
print("File Reading...")
points_gdf = gpd.read_file(input_path)

# Specify the buffer distance in the units of the shapefile's coordinate system
print(points_gdf.crs)  # print crs of point data

# Create a buffer around each point
print(f"Creating buffer of {buffer_distance}")
points_gdf['geometry'] = points_gdf.buffer(buffer_distance)

# Dissolve all buffers into a single geometry
print("Dissolving buffers...")
dissolved_points_gdf = points_gdf.union_all()

# Convert the dissolved geometry back into a GeoDataFrame for export and plotting
points_gdf = gpd.GeoDataFrame(geometry=[dissolved_points_gdf], crs=points_gdf.crs)

# Save the buffered geometry to a new shapefile
print(f"Saving buffer of {buffer_distance}")
points_gdf.to_file(output_path)

print(f"Buffered shapefile saved to: {output_path}")


# Plot to check the created buffer
# Set the Seaborn style
sns.set(style="whitegrid")  # You can choose other styles: darkgrid, whitegrid, dark, white, and ticks

# Plot the buffered geometries
fig, ax = plt.subplots(figsize=(10, 10))  # You can adjust the size as needed
points_gdf.plot(ax=ax, color='blue', alpha=0.5)  # Adjust color and transparency as needed

# Optional: Enhancements
ax.set_title('Buffered PWS', fontsize=15)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)

# Remove the x and y axis for a cleaner look
ax.set_xticks([])
ax.set_yticks([])

plt.get_current_fig_manager().toolbar.pan()  # This toggles the pan/zoom mode on
# Show the plot
plt.show()
