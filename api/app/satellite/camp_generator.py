
import json
from pathlib import Path

import geopandas as gpd
from shapely.geometry import box


def generate_sample_camps(
    output_path: Path,
    bounds: tuple[float, float, float, float],
    camp_count: int = 4,
) -> Path:
    """
    Generate artificial rectangular grazing camp polygons.

    Args:
        output_path: Where to save the GeoJSON file.
        bounds: (min_x, min_y, max_x, max_y) in EPSG:32733.
        camp_count: Number of sample camps to create.

    These polygons are for pipeline testing only.
    They do not represent real farm boundaries.
    """

    if camp_count < 1:
        raise ValueError("camp_count must be at least 1.")

    min_x, min_y, max_x, max_y = bounds

    if min_x >= max_x or min_y >= max_y:
        raise ValueError("Invalid spatial bounds.")

    width = (max_x - min_x) / camp_count
    height = max_y - min_y

    records = []

    for index in range(camp_count):
        left = min_x + index * width
        right = left + width

        geometry = box(
            left,
            min_y,
            right,
            max_y,
        )

        records.append({
            "camp_id": f"TEST_CAMP_{index + 1:03d}",
            "boundary_type": "SYNTHETIC_TEST",
            "geometry": geometry,
        })

    camps = gpd.GeoDataFrame(
        records,
        geometry="geometry",
        crs="EPSG:32733",
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    camps.to_file(output_path, driver="GeoJSON")

    return output_path
