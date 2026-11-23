
import numpy as np


# Sentinel-2 Scene Classification Layer (SCL) classes
INVALID_SCL_CLASSES = {
    0,   # No data
    1,   # Saturated or defective pixels
    3,   # Cloud shadows
    8,   # Medium probability clouds
    9,   # High probability clouds
    10,  # Thin cirrus
    11,  # Snow or ice
}


def create_cloud_mask(scl: np.ndarray) -> np.ndarray:
    """Create a Boolean mask from the Sentinel-2 SCL band.

    Returns:
        True  = valid pixel
        False = pixel excluded from analysis"""

    scl = np.asarray(scl)

    invalid_pixels = np.isin(
        scl,
        list(INVALID_SCL_CLASSES)
    )

    return ~invalid_pixels
