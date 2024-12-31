import rasterio
import numpy as np
import os


def calculate_tree_canopy_stats(folder_path):
    # Process each TIFF file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.tif'):
            file_path = os.path.join(folder_path, filename)

            # Open the raster file
            with rasterio.open(file_path) as src:
                # Total area of the raster in square units
                total_area = src.width * src.height * (src.res[0] * src.res[1])

                # Initialize variables for statistics
                total_coverage = 0
                sum_heights = np.float64(0)  # Ensure we use float64 to prevent overflow
                count_heights = 0
                max_height = float('-inf')
                min_height = float('inf')  # Initialize for calculating minimum height

                # Process the raster file in chunks
                for _, window in src.block_windows(1):
                    band1 = src.read(1, window=window)

                    # Mask to consider only the cells with tree canopies
                    canopy_mask = band1 > 0
                    canopy_heights = band1[canopy_mask]

                    # Update statistics
                    if canopy_heights.size > 0:
                        sum_heights += np.sum(canopy_heights, dtype=np.float64)  # Use float64 for summing
                        count_heights += canopy_heights.size
                        max_height = max(max_height, np.max(canopy_heights))
                        min_height = min(min_height, np.min(canopy_heights))

                    total_coverage += np.count_nonzero(canopy_mask) * (src.res[0] * src.res[1])

                # Compute overall statistics for the file
                mean_height = (sum_heights / count_heights) if count_heights > 0 else 0
                coverage_percent = (total_coverage / total_area) * 100 if total_area > 0 else 0

                # Print file-specific results
                print(f"File: {filename}")
                print(f"Min Height: {min_height:.3f} m")
                print(f"Mean Height: {mean_height:.3f} m")
                print(f"Max Height: {max_height:.3f} m")
                print(f"Total Coverage by Canopies: {total_coverage:.3f} sq. m")
                print(f"Total Area of Raster: {total_area:.3f} sq. m")
                print(f"Percentage of Coverage: {coverage_percent:.2f}%\n")


# Specify the folder containing the TIFF files
folder_path = r"E:\UAH_Classes\Research\Kansas\Canopy\Results"
calculate_tree_canopy_stats(folder_path)
