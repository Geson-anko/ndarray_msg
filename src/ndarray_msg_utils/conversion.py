from typing import Any

import numpy as np
import numpy.typing as npt
from ndarray_msg.msg import NDArray


def to_ros_msg(array: npt.NDArray[Any]) -> NDArray:
    """Convert a NumPy array to a ROS2 NDArray message.

    Serializes a NumPy array into a ROS2 NDArray message by storing its data type,
    shape, size and binary data. The array is flattened and converted to bytes
    for transmission.

    Args:
        array: Input NumPy array of any dimension and data type.

    Returns:
        A ROS2 NDArray message containing the serialized array data.

    Example:
        >>> import numpy as np
        >>> arr = np.array([[1, 2], [3, 4]])
        >>> msg = to_ros2_msg(arr)
    """
    msg = NDArray()
    msg.dtype = array.dtype.name
    msg.shape = list(array.shape)
    msg.data_size = array.size
    msg.data = [array.tobytes()]
    return msg


def from_ros_msg(msg: NDArray) -> npt.NDArray[Any]:
    """Convert a ROS2 NDarray message back to a NumPy array.

    Deserializes a ROS2 NDArray message into its original NumPy array form by
    reconstructing the array from its binary data using the stored dtype and shape
    information.

    Args:
        msg: Input ROS2 NDArray message containing serialized array data.

    Returns:
        The reconstructed NumPy array with original shape and data type.

    Example:
        >>> arr = from_ros_msg(ndarray_msg)
        >>> print(arr.shape)
        (2, 2)
    """
    array = np.frombuffer(msg.data[0], dtype=np.dtype(msg.dtype))
    return array.reshape(msg.shape)
