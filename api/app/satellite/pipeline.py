
import numpy as np

from app.satellite.cloud_mask import create_cloud_mask
from app.satellite.ndvi import calculate_ndvi


def process_satellite_bands(
    nir: np.ndarray,
    red: np.ndarray,
    scl: np.ndarray
) -> np.ndarray:
    """
    Apply cloud masking and calculate NDVI.

    Args:
        nir: Sentinel-2 Band 8 (Near Infrared).
        red: Sentinel-2 Band 4 (Red).
        scl: Sentinel-2 Scene Classification Layer.

    Returns:
        NDVI array with invalid pixels represented as NaN.
    """

    nir = np.asarray(nir, dtype=np.float32)
    red = np.asarray(red, dtype=np.float32)
    scl = np.asarray(scl)

    if nir.shape != red.shape or nir.shape != scl.shape:
        raise ValueError(
            "NIR, Red and SCL bands must have the same shape."
        )

    # Identify valid pixels using the SCL classification.
    valid_mask = create_cloud_mask(scl)

    # Replace invalid pixels with NaN.
    nir_clean = np.where(valid_mask, nir, np.nan)
    red_clean = np.where(valid_mask, red, np.nan)

    # Calculate NDVI using the cleaned bands.
    ndvi = calculate_ndvi(nir_clean, red_clean)

    return ndvi
