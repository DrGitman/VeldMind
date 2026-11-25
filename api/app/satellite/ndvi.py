
import numpy as np


def calculate_ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """
    Calculate the Normalized Difference Vegetation Index (NDVI).

    Sentinel-2:
        NIR = Band 8
        Red = Band 4

    NDVI = (NIR - Red) / (NIR + Red)
    """

    nir = np.asarray(nir, dtype=np.float32)
    red = np.asarray(red, dtype=np.float32)

    if nir.shape != red.shape:
        raise ValueError("NIR and Red bands must have the same shape.")

    denominator = nir + red

    ndvi = np.full(nir.shape, np.nan, dtype=np.float32)

    valid_pixels = (
    np.isfinite(nir)
    & np.isfinite(red)
    & (nir >= 0)
    & (red >= 0)
    & (denominator > 0)
    )

    np.divide(
        nir - red,
        denominator,
        out=ndvi,
        where=valid_pixels
    )

    return ndvi
