
import numpy as np
import pytest

from app.satellite.ndvi import calculate_ndvi


def test_calculate_ndvi_normal_values():
    nir = np.array([[0.8, 0.6]], dtype=np.float32)
    red = np.array([[0.2, 0.2]], dtype=np.float32)

    result = calculate_ndvi(nir, red)

    expected = np.array([[0.6, 0.5]], dtype=np.float32)

    np.testing.assert_allclose(result, expected, rtol=1e-6, atol=1e-7)


def test_calculate_ndvi_zero_denominator():
    nir = np.array([[0.0]], dtype=np.float32)
    red = np.array([[0.0]], dtype=np.float32)

    result = calculate_ndvi(nir, red)

    assert np.isnan(result[0, 0])


def test_calculate_ndvi_invalid_pixels():
    nir = np.array([[0.8, np.nan, np.inf]], dtype=np.float32)
    red = np.array([[0.2, 0.2, 0.1]], dtype=np.float32)

    result = calculate_ndvi(nir, red)

    assert np.isclose(result[0, 0], 0.6)
    assert np.isnan(result[0, 1])
    assert np.isnan(result[0, 2])


def test_calculate_ndvi_mismatched_shapes():
    nir = np.array([[0.8, 0.6]], dtype=np.float32)
    red = np.array([[0.2]], dtype=np.float32)

    with pytest.raises(ValueError):
        calculate_ndvi(nir, red)
