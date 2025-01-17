import geopandas as gpd
import pandas as pd
import os
import glob

# # Part A: Heights Extraction and Saving into csv
# # Directory containing the shapefiles
# directory = "E:\\UAH_Classes\\Research\\Kansas\\Buildings\\Heights"
#
# # List of suffixes for the shapefiles to process
# suffixes = ["20", "40", "60", "80", "100", "150", "200"]
#
# print(f'Extracting heights')
# # Loop through each suffix and extract height data from corresponding shapefiles
# heights_list = [
#     gpd.read_file(shp_file)['Height'] for suffix in suffixes
#     for shp_file in glob.glob(os.path.join(directory, f"*{suffix}.shp"))
#     if 'Height' in gpd.read_file(shp_file).columns
# ]
#
# # Create a DataFrame from the list of Series
# heights_df = pd.concat(heights_list, axis=1, keys=[f"PWS{s}" for s in suffixes])
# print(f'Heights extracted and concatenated')
#
# # Save the DataFrame to a CSV file in the same folder
# csv_file_path = os.path.join(directory, "Heights.csv")
# heights_df.to_csv(csv_file_path, index=False)
#
# print(f"Data saved to {csv_file_path}")
# # End of Part A

# Part B: Read Heights and Prepare bean plots
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics import beanplot

# Path to the CSV file
csv_file_path = "E:\\UAH_Classes\\Research\\Kansas\\Buildings\\Heights\\Heights.csv"

# Read the CSV file into a DataFrame
heights_df = pd.read_csv(csv_file_path)

# Prepare data for the beanplot - extracting each series of heights
height_data = [heights_df[col].dropna().values for col in heights_df.columns]

# Create the figure and axis objects
plt.figure(figsize=(12, 8))

# Create a beanplot
beanplot.beanplot(height_data, labels=heights_df.columns, show_means=False, show_median=True, side='both')

# Customize plot
plt.title('Beanplot of PWS Buffers vs Height')
plt.xlabel('PWS Buffer')
plt.ylabel('Height (meters)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

# Show the plot
plt.tight_layout()
plt.show()
