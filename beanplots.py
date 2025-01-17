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
import numpy as np
import statsmodels.api as sm
import geopandas as gpd
import os
import glob

# Assuming the height data has been successfully extracted and saved
# Read the CSV file into a DataFrame
csv_file_path = "E:\\UAH_Classes\\Research\\Kansas\\Buildings\\Heights\\Building_Reflectance.csv"
heights_df = pd.read_csv(csv_file_path)

# Prepare data for the beanplot - extracting each series of heights
height_data = [heights_df[col].dropna().values for col in heights_df.columns]

# plt.rcParams['figure.subplot.bottom'] = 0.8  # keep labels visible

# Create the figure and axis objects
fig, ax = plt.subplots(figsize=(12, 8))

# Define plot options
plot_opts = {
    'bean_lw':0.5,
    'violin_width':0.75,
    'cutoff':True,
    'cutoff_val': 5,  # Absolute cutoff for bean width
    'cutoff_type': 'std',  # Type of cutoff, 'abs' for absolute value cutoff
    'label_fontsize': 'small',  # Font size for labels
    'bean_show_meadian':True,
    'jitter_marker_size':1,
    'bean_legend_text':'Reflectance'
}

# Create a beanplot
sm.graphics.beanplot(height_data, labels=heights_df.columns, side='both', jitter=True, plot_opts=plot_opts, ax=ax)

# Manually add median lines
# for i, data in enumerate(height_data):
#     median_val = np.median(data)
#     ax.plot([i + 1], [median_val], 'wo')  # 'wo' stands for white circle marker

# Customize plot
ax.set_title('Beanplot of Building Reflectance within PWS Buffer')
ax.set_xlabel('PWS Buffer Distance')
ax.set_ylabel('Building Reflectance')

# Setting y-axis ticks to show only some representative values
max_height = max([max(data) for data in height_data if len(data) > 0])
min_height = min([min(data) for data in height_data if len(data) > 0])
# You can adjust the 'num' parameter to increase or decrease the number of ticks
ax.set_yticks(np.linspace(min_height, max_height, num=6))

# Set custom x-tick labels with rotation for better readability
ax.set_xticklabels(heights_df.columns, rotation=45)

# Show the plot
plt.tight_layout()
plt.show()
