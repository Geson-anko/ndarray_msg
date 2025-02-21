import numpy as np
import pytest

from ndarray_msg_utils.conversion import from_ros_msg, to_ros_msg


def test_conversion_int32():
    """Test conversion with int32 arrays."""
    original = np.array([[1, 2], [3, 4]], dtype=np.int32)
    msg = to_ros_msg(original)
    restored = from_ros_msg(msg)

    assert msg.dtype == "int32"
    assert list(msg.shape) == [2, 2]
    assert msg.data_size == 4
    np.testing.assert_array_equal(original, restored)


def test_conversion_float64():
    """Test conversion with float64 arrays."""
    original = np.array([1.5, 2.5, 3.5], dtype=np.float64)
    msg = to_ros_msg(original)
    restored = from_ros_msg(msg)

    assert msg.dtype == "float64"
    assert list(msg.shape) == [3]
    assert msg.data_size == 3
    np.testing.assert_array_equal(original, restored)


def test_empty_array():
    """Test conversion with empty arrays."""
    original = np.array([], dtype=np.float32)
    msg = to_ros_msg(original)
    restored = from_ros_msg(msg)

    assert msg.dtype == "float32"
    assert list(msg.shape) == [0]
    assert msg.data_size == 0
    np.testing.assert_array_equal(original, restored)


def test_multidimensional_array():
    """Test conversion with multidimensional arrays."""
    original = np.ones((2, 3, 4), dtype=np.float32)
    msg = to_ros_msg(original)
    restored = from_ros_msg(msg)

    assert list(msg.shape) == [2, 3, 4]
    assert msg.data_size == 24
    np.testing.assert_array_equal(original, restored)


def test_boolean_array():
    """Test conversion with boolean arrays."""
    original = np.array([[True, False], [False, True]])
    msg = to_ros_msg(original)
    restored = from_ros_msg(msg)

    assert msg.dtype == "bool"
    np.testing.assert_array_equal(original, restored)


@pytest.mark.parametrize(
    "dtype",
    [
        np.int8,
        np.int16,
        np.int32,
        np.int64,
        np.uint8,
        np.uint16,
        np.uint32,
        np.uint64,
        np.float32,
        np.float64,
    ],
)
def test_various_dtypes(dtype):
    """Test conversion with various numeric dtypes."""
    original = np.array([[1, 2], [3, 4]], dtype=dtype)
    msg = to_ros_msg(original)
    restored = from_ros_msg(msg)

    assert msg.dtype == dtype.__name__
    np.testing.assert_array_equal(original, restored)


def test_non_contiguous_array():
    """Test conversion with non-contiguous arrays."""
    original = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int32)
    # Create non-contiguous array by transposing
    non_contiguous = original.T
    assert not non_contiguous.flags["C_CONTIGUOUS"]

    msg = to_ros_msg(non_contiguous)
    restored = from_ros_msg(msg)

    np.testing.assert_array_equal(non_contiguous, restored)
