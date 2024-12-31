# This code computes the area of all polygons in a shp.
# # Also calculates mean height of polygons if there is height field
import geopandas as gpd
import os

def calculate_area_and_height(folder_path):
    # List all shapefiles in the specified folder
    shapefiles = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.shp')]

    # Process each shapefile
    for shp in shapefiles:
        print(f"Processing {shp}...")
        # Load the shapefile
        gdf = gpd.read_file(shp)

        # Calculate area of each polygon (area is returned in square units of the CRS)
        gdf['Area'] = gdf['geometry'].area

        # Check if 'Height' field exists in the dataframe
        if 'Height' in gdf.columns:
            # Calculate the average height
            average_height = gdf['Height'].mean()
            print(f"Average Height for {shp}: round({average_height}, 3) m")
        else:
            print(f"No 'Height' field found in {shp}")

        # Print area of each polygon
        print("Area of each polygon (in square m):")
        print(round(gdf['Area'], 4))

        # Optionally, save the GeoDataFrame back to a shapefile with the new 'Area' field
        # output_filename = os.path.splitext(shp)[0] + '_with_area.shp'
        # gdf.to_file(output_filename)
        # print(f"Updated shapefile saved to: {output_filename}")

# Specify the folder containing the shapefiles
folder_path = r"E:\UAH_Classes\Research\Kansas\Buildings\Heights"  # path to the directory containing shapefiles
calculate_area_and_height(folder_path)
