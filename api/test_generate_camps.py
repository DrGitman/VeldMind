
from pathlib import Path

import rasterio

from app.satellite.camp_generator import generate_sample_camps


raster_path = Path("data/outputs/windhoek_ndvi_20261116.tif")

output_path = Path("data/outputs/sample_camps.geojson")

# Read the actual raster bounds.
with rasterio.open(raster_path) as dataset:
    bounds = dataset.bounds

    # Select the central 40% of the raster.
    width = bounds.right - bounds.left
    height = bounds.top - bounds.bottom

    min_x = bounds.left + width * 0.30
    max_x = bounds.left + width * 0.70

    min_y = bounds.bottom + height * 0.30
    max_y = bounds.bottom + height * 0.70

    sample_bounds = (min_x, min_y, max_x, max_y)

# Generate four artificial camps.
result = generate_sample_camps(
    output_path=output_path,
    bounds=sample_bounds,
    camp_count=4,
)

print("Sample camps generated successfully!")
print(f"Output: {result}")
print(f"Bounds: {sample_bounds}")
