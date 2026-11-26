
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask


def calculate_camp_statistics(
    ndvi_path: Path,
    camps_path: Path,
    vegetation_threshold: float = 0.3,
) -> list[dict]:
    """
    Calculate NDVI statistics for each grazing camp polygon.

    Vegetation coverage is the percentage of valid pixels
    with NDVI greater than or equal to the threshold.

    Synthetic camp boundaries can be used for testing.
    """

    ndvi_path = Path(ndvi_path)
    camps_path = Path(camps_path)

    camps = gpd.read_file(camps_path)

    if camps.empty:
        raise ValueError("No camp polygons found.")

    if "camp_id" not in camps.columns:
        raise ValueError("Camp data must contain a camp_id column.")

    results = []

    with rasterio.open(ndvi_path) as dataset:

        # Ensure camp polygons use the raster's CRS.
        if camps.crs is None:
            raise ValueError("Camp polygons have no CRS.")

        if camps.crs != dataset.crs:
            camps = camps.to_crs(dataset.crs)

        for _, camp in camps.iterrows():

            geometry = camp.geometry

            if geometry is None or geometry.is_empty:
                raise ValueError(
                    f"Invalid geometry for {camp['camp_id']}"
                )

            try:
                masked_data, _ = mask(
                    dataset,
                    [geometry],
                    crop=True,
                    filled=False,
                )
            except ValueError as exc:
                raise ValueError(
                    f"Camp {camp['camp_id']} does not overlap the NDVI raster."
                ) from exc

            # Extract valid, finite NDVI pixels.
            pixels = masked_data[0].compressed()
            pixels = pixels[np.isfinite(pixels)]

            if pixels.size == 0:
                results.append({
                    "camp_id": camp["camp_id"],
                    "boundary_type": camp.get("boundary_type"),
                    "valid_pixel_count": 0,
                    "vegetation_pixel_count": 0,
                    "mean_ndvi": None,
                    "median_ndvi": None,
                    "min_ndvi": None,
                    "max_ndvi": None,
                    "vegetation_coverage_pct": None,
                })
                continue

            vegetation_pixels = pixels[
                pixels >= vegetation_threshold
            ]

            results.append({
                "camp_id": camp["camp_id"],
                "boundary_type": camp.get("boundary_type"),
                "valid_pixel_count": int(pixels.size),
                "vegetation_pixel_count": int(
                    vegetation_pixels.size
                ),
                "mean_ndvi": float(np.mean(pixels)),
                "median_ndvi": float(np.median(pixels)),
                "min_ndvi": float(np.min(pixels)),
                "max_ndvi": float(np.max(pixels)),
                "vegetation_coverage_pct": float(
                    vegetation_pixels.size / pixels.size * 100
                ),
            })

    return results
