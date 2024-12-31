import rasterio
import numpy as np
import matplotlib.pyplot as plt

def compute_tree_canopy_metrics(raster_path):
    with rasterio.open(raster_path) as src:
        print(f"Opening file ...")
        # Initialize metrics
        total_pixels = 0.0
        canopy_pixels = 0.0
        total_height = 0.0  # Use float64 to avoid overflow
        total_canopy_coverage = 0.0
        max_height = float('-inf')  # Initialize to negative infinity for max height tracking
        min_height = float('inf')   # Initialize to positive infinity for min height tracking

        # Process the raster in windows
        for window in src.block_windows(1):
            print(f"Reading file ...")
            heights = src.read(1, window=window[1]).astype(np.float64)  # Read data in the current window as float64
            nodata = 128
            valid_data_mask = (heights != nodata)

            # Mask for canopy pixels
            canopy_mask = (heights > 0) & valid_data_mask
            total_pixels += valid_data_mask.sum()
            canopy_pixels += canopy_mask.sum()

            # Update min and max heights within valid canopy heights
            print("Calculating min and max heights ...")
            if np.any(canopy_mask):  # Check if there's any canopy pixel in the current window
                max_height = max(max_height, np.max(heights[canopy_mask]))
                min_height = min(min_height, np.min(heights[canopy_mask]))

            # Sum heights where there are valid canopy pixels
            total_height += np.sum(heights[canopy_mask])

            # Compute canopy coverage in the current window
            total_canopy_coverage += canopy_mask.sum() * (src.res[0] * src.res[1])

        # Calculate overall metrics
        print(f"Still calculating ...")
        total_area = total_pixels * (src.res[0] * src.res[1])
        percentage_coverage = (total_canopy_coverage / total_area) * 100
        mean_height = total_height / total_pixels if total_pixels else 0

        print(f"Min Height: {min_height if min_height != float('inf') else 'No canopy pixels found'} meters")
        print(f"Max Height: {max_height if max_height != float('-inf') else 'No canopy pixels found'} meters")
        print(f"Mean Height: {mean_height} meters")
        print(f"Total Coverage by Tree Canopies: {total_canopy_coverage} square meters")
        print(f"Percentage of Coverage by Tree Canopies: {percentage_coverage}%")

    return heights, canopy_mask, total_pixels, canopy_pixels, min_height, max_height

# Path to your TIFF file
raster_path = r"E:\UAH_Classes\Research\Kansas\Canopy\Results\kansasCanopy200.tif"
heights, mask, total_pixels, canopy_pixels, min_height, max_height = compute_tree_canopy_metrics(raster_path)
