import rasterio
import numpy as np
import matplotlib.pyplot as plt


def compute_tree_canopy_metrics(raster_path):
    # Open the raster file
    with rasterio.open(raster_path) as src:
        # Read the first band (assuming height data is in the first band)
        canopy_heights = src.read(1)

        # Calculate non-zero (tree canopy) coverage
        canopy_mask = canopy_heights > 0  # Change 0 to the appropriate threshold if different
        total_pixels = canopy_heights.size
        canopy_pixels = np.count_nonzero(canopy_mask)
        total_canopy_coverage = canopy_pixels * src.res[0] * src.res[1]  # Total area in square meters
        percentage_coverage = (canopy_pixels / total_pixels) * 100

        # Compute statistics
        max_height = np.max(canopy_heights)
        mean_height = np.mean(canopy_heights[canopy_mask])  # Mean over canopy areas only

        print(f"Max Height: {max_height} meters")
        print(f"Mean Height: {mean_height} meters")
        print(f"Average Coverage: {total_canopy_coverage / total_pixels} square meters per pixel")
        print(f"Total Coverage by Tree Canopies: {total_canopy_coverage} square meters")
        print(f"Percentage of Coverage by Tree Canopies: {percentage_coverage}%")

        # Optional: visualize the raster
        plt.imshow(canopy_heights, cmap='viridis')
        plt.colorbar(label='Height (m)')
        plt.title('Tree Canopy Heights')
        plt.xlabel('Pixel X Coordinate')
        plt.ylabel('Pixel Y Coordinate')
        plt.show()


# Path to your TIFF file
raster_path = r"E:\UAH_Classes\Research\Kansas\Canopy\Results\kansasCanopy20.tif"
compute_tree_canopy_metrics(raster_path)
