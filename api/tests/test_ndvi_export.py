
import numpy as np
import rasterio

from app.satellite.ndvi_export import export_ndvi_geotiff


def test_export_ndvi_geotiff(tmp_path):
    reference_path = tmp_path / "reference_scl.tif"
    output_path = tmp_path / "ndvi.tif"

    transform = rasterio.transform.from_origin(
        500000, 7500000, 20, 20
    )

    # Create a small reference SCL raster.
    with rasterio.open(
        reference_path,
        "w",
        driver="GTiff",
        height=3,
        width=3,
        count=1,
        dtype="uint8",
        crs="EPSG:32733",
        transform=transform,
    ) as dataset:
        dataset.write(
            np.ones((3, 3), dtype=np.uint8),
            1,
        )

    ndvi = np.array(
        [
            [0.2, 0.4, 0.6],
            [0.1, np.nan, 0.8],
            [-0.2, 0.3, 0.5],
        ],
        dtype=np.float32,
    )

    result = export_ndvi_geotiff(
        ndvi,
        reference_path,
        output_path,
    )

    assert result.exists()

    with rasterio.open(result) as dataset:
        assert dataset.crs.to_string() == "EPSG:32733"
        assert dataset.width == 3
        assert dataset.height == 3
        assert dataset.dtypes[0] == "float32"
        assert np.isnan(dataset.read(1)[1, 1])
        assert dataset.nodata is not None
