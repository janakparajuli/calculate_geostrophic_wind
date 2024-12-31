import rasterio
import numpy as np
import matplotlib.pyplot as plt

def compute_tree_canopy_metrics(raster_path):
    with rasterio.open(raster_path) as src:
        # Initialize metrics
        total_pixels = 0
        canopy_pixels = 0
        total_height = 0.0  # Use float64 to avoid overflow
        total_canopy_coverage = 0.0

        # Process the raster in windows
        for window in src.block_windows(1):
            heights = src.read(1, window=window[1]).astype(np.float64)  # Read data in the current window as float64
            nodata = -128
            valid_data_mask = (heights != nodata)

            # Mask for canopy pixels
            canopy_mask = (heights > 1) & valid_data_mask
            total_pixels += valid_data_mask.sum()
            canopy_pixels += canopy_mask.sum()

            # Sum heights where there are valid canopy pixels
            total_height += np.sum(heights[canopy_mask])

            # Compute canopy coverage in the current window
            total_canopy_coverage += canopy_mask.sum() * (src.res[0] * src.res[1])

        # Calculate overall metrics
        total_area = total_pixels * (src.res[0] * src.res[1])
        percentage_coverage = (total_canopy_coverage / total_area) * 100
        mean_height = total_height / canopy_pixels if canopy_pixels else 0

        print(f"Mean Height: {mean_height} meters")
        print(f"Total Coverage by Tree Canopies: {total_canopy_coverage} square meters")
        print(f"Percentage of Coverage by Tree Canopies: {percentage_coverage}%")

        # Optional: visualize the last processed chunk
        plt.imshow(heights, cmap='viridis', vmin=1)
        plt.colorbar(label='Height (m)')
        plt.title('Last Chunk of Tree Canopy Heights')
        plt.xlabel('Pixel X Coordinate')
        plt.ylabel('Pixel Y Coordinate')
        plt.show()

    return heights, canopy_mask, total_pixels, canopy_pixels

# Path to your TIFF file
raster_path = r"E:\UAH_Classes\Research\Kansas\Canopy\Results\kansasCanopy20.tif"
compute_tree_canopy_metrics(raster_path)
