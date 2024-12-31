# Computes area and heights of tree canopies

import rasterio
import numpy as np
import os

def calculate_tree_canopy_stats(folder_path):
    # List to hold canopy heights from all files for overall stats
    # all_canopy_heights = []

    # Process each TIFF file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.tif'):
            file_path = os.path.join(folder_path, filename)

            # Open the raster file
            with rasterio.open(file_path) as src:
                # Read the first band (assuming height values are in the first band)
                band1 = src.read(1)

                # Mask to consider only the cells with tree canopies (assuming height > 0 indicates presence of canopy)
                canopy_mask = band1 > 0
                canopy_heights = band1[canopy_mask]

                # Calculate statistics
                min_height = canopy_heights.min() if canopy_heights.size > 0 else 0
                mean_height = canopy_heights.mean() if canopy_heights.size > 0 else 0
                max_height = canopy_heights.max() if canopy_heights.size > 0 else 0
                total_coverage = np.count_nonzero(canopy_mask) * \
                            (src.res[0] * src.res[1])  # Total covered area in square units
                area = src.width * src.height * (src.res[0] * src.res[1])  # Total area of the raster in square units

                # Append to all heights for overall statistics
                # all_canopy_heights.extend(canopy_heights.tolist())

                # Print file-specific results
                print(f"File: {filename}")
                print(f"Mean Height: {min_height:.3f} m")
                print(f"Mean Height: {mean_height:.3f} m")
                print(f"Max Height: {max_height:.3f} m")
                print(f"Total Coverage by Canopies: {total_coverage:.3f} sq. m")
                print(f"Total Coverage by Buffer: {area:.3f} sq. m")
                print(f"Percentage of Coverage: {(total_coverage / area) * 100:.2f}%\n")

    # Calculate overall statistics
    # if all_canopy_heights:
    #     overall_mean_height = np.mean(all_canopy_heights)
    #     overall_max_height = np.max(all_canopy_heights)
    #     print(f"Overall Mean Height of Canopies: {overall_mean_height:.2f}")
    #     print(f"Overall Max Height of Canopies: {overall_max_height:.2f}")


# Specify the folder containing the TIFF files
folder_path = r"E:\UAH_Classes\Research\Kansas\Canopy\Results"
calculate_tree_canopy_stats(folder_path)
