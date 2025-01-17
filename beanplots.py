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
import seaborn as sns
import matplotlib.pyplot as plt

# Path to the CSV file
csv_file_path = "E:\\UAH_Classes\\Research\\Kansas\\Buildings\\Heights\\Heights.csv"

# Read the CSV file into a DataFrame
heights_df = pd.read_csv(csv_file_path)

# Melt the DataFrame to make it suitable for seaborn's plotting functions
melted_df = heights_df.melt(var_name='PWS_Buffer', value_name='Height')

# Plotting the beanplot using seaborn's violin plot, which is similar to a beanplot
plt.figure(figsize=(12, 8))
sns.violinplot(x='PWS_Buffer', y='Height', data=melted_df, inner='stick', density_norm='width')
plt.title('Beanplot of PWS Buffers vs Height')
plt.xlabel('PWS Buffer')
plt.ylabel('Height (meters)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()

# Show the plot
plt.show()
