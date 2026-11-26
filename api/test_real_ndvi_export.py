
from pathlib import Path

import numpy as np
import rasterio

from app.satellite.raster_loader import load_sentinel2_bands
from app.satellite.pipeline import process_satellite_bands
from app.satellite.ndvi_export import export_ndvi_geotiff


scene_dir = Path("data/sentinel2/Windhoek_scene_02")

scl_path = next(scene_dir.glob("*_SCL_20m.jp2"))

print("Loading Sentinel-2 bands...")

nir, red, scl = load_sentinel2_bands(scene_dir)

print("Calculating NDVI...")

ndvi = process_satellite_bands(nir, red, scl)

output_path = Path("data/outputs/windhoek_ndvi_20261116.tif")

print("Exporting NDVI GeoTIFF...")

export_ndvi_geotiff(ndvi, scl_path, output_path)

with rasterio.open(output_path) as dataset:
    exported = dataset.read(1)
    valid = np.isfinite(exported)

    print("\nExport validation")
    print("-----------------")
    print(f"Output: {output_path}")
    print(f"CRS: {dataset.crs}")
    print(f"Resolution: {dataset.res}")
    print(f"Dimensions: {dataset.width} x {dataset.height}")
    print(f"Valid pixels: {valid.sum():,}")
    print(f"Invalid pixels: {(~valid).sum():,}")
    print(f"Minimum NDVI: {np.nanmin(exported):.4f}")
    print(f"Maximum NDVI: {np.nanmax(exported):.4f}")
    print(f"Mean NDVI: {np.nanmean(exported):.4f}")
    print(f"NoData: {dataset.nodata}")
