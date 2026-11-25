
from pathlib import Path

import numpy as np
import rasterio


def export_ndvi_geotiff(
    ndvi: np.ndarray,
    reference_scl_path: Path,
    output_path: Path,
) -> Path:
    """
    Export an NDVI array as a georeferenced GeoTIFF.

    The SCL raster provides the spatial metadata because
    the NDVI array is aligned to the SCL grid.
    """

    ndvi = np.asarray(ndvi, dtype=np.float32)

    with rasterio.open(reference_scl_path) as reference:
        if ndvi.shape != (reference.height, reference.width):
            raise ValueError(
                "NDVI dimensions must match the reference SCL raster."
            )

        profile = reference.profile.copy()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    profile.update(
        driver="GTiff",
        dtype="float32",
        count=1,
        nodata=np.nan,
        compress="deflate",
        predictor=3,
    )

    with rasterio.open(output_path, "w", **profile) as destination:
        destination.write(ndvi, 1)
        destination.set_band_description(1, "NDVI")

    return output_path
