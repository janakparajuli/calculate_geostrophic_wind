# This code merges tiff files with same extent into one tiff

# Define function to find max reflectance values
import numpy as np


def max_merge_method(old_data, new_data, old_nodata, new_nodata, index=None):
    """
    Custom merge function to take the maximum value where datasets overlap.
    Assumes that the nodata values are marked identically in both datasets.
    """
    # Create a mask where either the old data or new data is not nodata
    mask = (old_data != old_nodata) & (new_data != new_nodata)

    # Use maximum value from old and new data where mask is True
    max_data = np.maximum(old_data, new_data)

    # Where the mask is False, keep the old data values (preserve existing data)
    return np.where(mask, max_data, old_data)
