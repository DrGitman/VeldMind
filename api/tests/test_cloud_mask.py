import numpy as np

from app.satellite.cloud_mask import create_cloud_mask


def test_cloud_mask_excludes_clouds():
    scl = np.array([[4, 8, 9]])
    result = create_cloud_mask(scl)
    expected = np.array([[True, False, False]])
    np.testing.assert_array_equal(result, expected)


def test_cloud_mask_excludes_cloud_shadows():
    scl = np.array([[4, 3, 5]])
    result = create_cloud_mask(scl)
    expected = np.array([[True, False, True]])
    np.testing.assert_array_equal(result, expected)


def test_cloud_mask_retains_valid_classes():
    scl = np.array([[2, 4, 5, 6, 7]])
    result = create_cloud_mask(scl)
    expected = np.array([[True, True, True, True, True]])
    np.testing.assert_array_equal(result, expected)


def test_cloud_mask_preserves_dimensions():
    scl = np.array([[4, 8, 9], [5, 3, 6]])
    result = create_cloud_mask(scl)
    assert result.shape == scl.shape
