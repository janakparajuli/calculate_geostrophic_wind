import rasterio
import numpy as np
import matplotlib.pyplot as plt

def compute_tree_canopy_metrics(raster_path):
    with rasterio.open(raster_path) as src:
        print("Raster metadata:", src.meta)  # Print metadata to verify data type and no data values

        # Preparing to read data correctly
        data_type = src.dtypes[0]
        print(f"Data type of the raster: {data_type}")

        # Read the entire raster data for processing
        canopy_heights = src.read(1)

        # If data is read as all the same value (128), check if a scale or offset needs to be applied
        if np.unique(canopy_heights).size == 1:  # Only one unique value found
            print("Warning: Only one unique value found in data, please check the correctness of the read operation")

        # Process data
        # Mask for canopy pixels, assuming no data is not using 0 height and actual data starts from height > 1
        canopy_mask = canopy_heights > 1
        total_pixels = canopy_heights.size
        canopy_pixels = np.count_nonzero(canopy_mask)

        total_height = np.sum(canopy_heights[canopy_mask])
        total_canopy_coverage = canopy_pixels * (src.res[0] * src.res[1])

        # Calculate metrics
        total_area = total_pixels * (src.res[0] * src.res[1])
        percentage_coverage = (total_canopy_coverage / total_area) * 100
        mean_height = total_height / canopy_pixels if canopy_pixels else 0

        print(f"Mean Height: {mean_height} meters")
        print(f"Total Coverage by Tree Canopies: {total_canopy_coverage} square meters")
        print(f"Percentage of Coverage by Tree Canopies: {percentage_coverage}%")

        # Optional: visualize the raster
        plt.imshow(canopy_heights, cmap='viridis', vmin=1)  # setting vmin to 1 to avoid showing non-canopy areas
        plt.colorbar(label='Height (m)')
        plt.title('Tree Canopy Heights')
        plt.xlabel('Pixel X Coordinate')
        plt.ylabel('Pixel Y Coordinate')
        plt.show()

    return canopy_heights, canopy_mask, total_pixels, canopy_pixels

# Path to your TIFF file
raster_path = r"E:\UAH_Classes\Research\Kansas\Canopy\Results\kansasCanopy20.tif"
compute_tree_canopy_metrics(raster_path)
