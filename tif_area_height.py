import rasterio
import numpy as np
import matplotlib.pyplot as plt


def compute_tree_canopy_metrics(raster_path):
    with rasterio.open(raster_path) as src:
        print("Raster dtype:", src.dtypes)  # Print the data type of the raster
        total_pixels = 0
        canopy_pixels = 0
        total_height = 0.0
        total_canopy_coverage = 0.0

        for ji, window in src.block_windows(1):
            heights = src.read(1, window=window)  # Read data without conversion
            print("Unique heights before conversion:", np.unique(heights))  # Debug line

            # Convert data type if necessary
            if heights.dtype != np.float64:
                heights = heights.astype(np.float64)

            mask = heights > 1
            total_pixels += heights.size
            canopy_pixels += mask.sum()
            total_height += heights[mask].sum()
            total_canopy_coverage += mask.sum() * src.res[0] * src.res[1]

        total_area = total_pixels * src.res[0] * src.res[1]
        percentage_coverage = (total_canopy_coverage / total_area) * 100
        mean_height = total_height / canopy_pixels if canopy_pixels else 0

        print("Min Height:", heights.min(), "meters")
        print("Max Height:", heights.max(), "meters")
        print("Mean Height:", mean_height, "meters")
        print("Total Coverage by Tree Canopies:", total_canopy_coverage, "square meters")
        print("Percentage of Coverage by Tree Canopies:", percentage_coverage, "%")

    return heights, mask, total_pixels, canopy_pixels


# Path to your TIFF file
raster_path = r"E:\UAH_Classes\Research\Kansas\Canopy\Results\kansasCanopy20.tif"
ht, mask, tot_pxl, cnp_pxl = compute_tree_canopy_metrics(raster_path)
