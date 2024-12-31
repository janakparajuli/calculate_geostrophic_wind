# This code computes the area of all polygons in a shp.
# # Also calculates mean height of polygons if there is height field
import geopandas as gpd
import os

def calculate_area_and_height(folder_path):
    # List all shapefiles in the specified folder
    shapefiles = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('0.shp')]

    # Process each shapefile
    for shp in shapefiles:
        print(f"Processing {shp}...")
        # Load the shapefile
        gdf = gpd.read_file(shp)

        print(".........")
        # Calculate the number of polygons
        num_polygons = len(gdf)
        print(f"Number of polygons in {shp}: {num_polygons}")

        # Calculate area of each polygon
        gdf['Area'] = gdf['geometry'].area
        mean_area = gdf['Area'].mean()
        print(f"Mean Area for {shp}: {round(mean_area, 4)} sq. m")

        # Calculate total area of each shp
        sum_area = gdf['Area'].sum()
        print(f"Total Footprint Area for {shp}: {round(sum_area, 4)} sq. m")

        # Check if 'Height' field exists in the dataframe
        if 'Height' in gdf.columns:
            mean_height = gdf['Height'].mean()
            print(f"Mean Height for {shp}: {round(mean_height, 3)} m")
        else:
            print(f"No 'Height' field found in {shp}")

        # Optionally, save the GeoDataFrame back to a shapefile with the new 'Area' field
        # output_filename = os.path.splitext(shp)[0] + '_with_area.shp'
        # gdf.to_file(output_filename)
        # print(f"Updated shapefile saved to: {output_filename}")

# Specify the folder containing the shapefiles
folder_path = r"E:\UAH_Classes\Research\Kansas\Buildings\Heights"  # path to the directory containing shapefiles
calculate_area_and_height(folder_path)
