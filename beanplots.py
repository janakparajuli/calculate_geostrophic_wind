import geopandas as gpd
import pandas as pd
import os
import glob

# Directory containing the shapefiles
directory = "E:\\UAH_Classes\\Research\\Kansas\\Buildings\\Heights"

# List of suffixes for the shapefiles to process
suffixes = ["20", "40", "60", "80", "100", "150", "200"]

# Loop through each suffix and extract height data from corresponding shapefiles
heights_list = [
    gpd.read_file(shp_file)['Height'] for suffix in suffixes
    for shp_file in glob.glob(os.path.join(directory, f"*{suffix}.shp"))
    if 'Height' in gpd.read_file(shp_file).columns
]

# Create a DataFrame from the list of Series
heights_df = pd.concat(heights_list, axis=1, keys=[f"PWS{s}" for s in suffixes])

# Save the DataFrame to a CSV file in the same folder
csv_file_path = os.path.join(directory, "Heights.csv")
heights_df.to_csv(csv_file_path, index=False)

print(f"Data saved to {csv_file_path}")
