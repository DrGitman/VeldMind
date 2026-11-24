
import numpy as np
import pytest

from app.satellite.pipeline import process_satellite_bands


def test_pipeline_calculates_ndvi():
    nir = np.array([[0.8, 0.6]], dtype=np.float32)
    red = np.array([[0.2, 0.2]], dtype=np.float32)
    scl = np.array([[4, 5]])

    result = process_satellite_bands(nir, red, scl)

    expected = np.array([[0.6, 0.5]], dtype=np.float32)

    np.testing.assert_allclose(
        result, expected, rtol=1e-6, atol=1e-7
    )


def test_pipeline_excludes_cloud_pixels():
    nir = np.array([[0.8, 0.8, 0.6]], dtype=np.float32)
    red = np.array([[0.2, 0.2, 0.2]], dtype=np.float32)
    scl = np.array([[4, 9, 5]])

    result = process_satellite_bands(nir, red, scl)

    assert np.isfinite(result[0, 0])
    assert np.isnan(result[0, 1])
    assert np.isfinite(result[0, 2])


def test_pipeline_excludes_cloud_shadows():
    nir = np.array([[0.8, 0.7]], dtype=np.float32)
    red = np.array([[0.2, 0.3]], dtype=np.float32)
    scl = np.array([[4, 3]])

    result = process_satellite_bands(nir, red, scl)

    assert np.isfinite(result[0, 0])
    assert np.isnan(result[0, 1])


def test_pipeline_rejects_mismatched_shapes():
    nir = np.array([[0.8, 0.6]])
    red = np.array([[0.2, 0.2]])
    scl = np.array([[4, 5, 9]])

    with pytest.raises(ValueError):
        process_satellite_bands(nir, red, scl)
