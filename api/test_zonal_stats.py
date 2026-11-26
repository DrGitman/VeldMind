
from pathlib import Path

from app.satellite.zonal_stats import calculate_camp_statistics
from app.satellite.statistics_export import export_camp_statistics

ndvi_path = Path("data/outputs/windhoek_ndvi_20261116.tif")
camps_path = Path("data/outputs/sample_camps.geojson")

results = calculate_camp_statistics(
    ndvi_path=ndvi_path,
    camps_path=camps_path,
    vegetation_threshold=0.3,
)

output_path = Path(
    "data/outputs/camp_statistics_20261116.json"
)

export_camp_statistics(
    statistics=results,
    output_path=output_path,
    observation_date="2026-11-16",
    satellite="Sentinel-2",
    vegetation_threshold=0.3,
)

print(f"\nJSON export successful: {output_path}")

print("\nCAMP NDVI STATISTICS")
print("=" * 65)

for result in results:
    print(f"\nCamp: {result['camp_id']}")
    print(f"Boundary type: {result['boundary_type']}")
    print(f"Valid pixels: {result['valid_pixel_count']}")
    print(f"Vegetation pixels: {result['vegetation_pixel_count']}")
    print(f"Mean NDVI: {result['mean_ndvi']}")
    print(f"Median NDVI: {result['median_ndvi']}")
    print(f"Minimum NDVI: {result['min_ndvi']}")
    print(f"Maximum NDVI: {result['max_ndvi']}")
    print(
        "Vegetation coverage: "
        f"{result['vegetation_coverage_pct']}%"
    )
