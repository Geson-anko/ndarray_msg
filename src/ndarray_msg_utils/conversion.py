from typing import Any

import numpy as np
import numpy.typing as npt
from ndarray_msg.msg import NDArray
from rclpy.time import Time
from std_msgs.msg import Header

from .utils import get_now_time


def to_ros_msg(
    array: npt.NDArray[Any], timestamp: Time | None = None, frame_id: str = ""
) -> NDArray:
    """Convert a NumPy array to a ROS2 NDArray message.

    Serializes a NumPy array into a ROS2 NDArray message by storing its data type,
    shape, size and binary data. The array is flattened and converted to bytes
    for transmission. Includes ROS header with timestamp and frame_id.

    Args:
        array: Input NumPy array of any dimension and data type.
        timestamp: ROS Time object for header timestamp. If None, current time is used.
        frame_id: Frame ID string for header. Empty string by default.

    Returns:
        A ROS2 NDArray message containing the serialized array data and header.

    Example:
        >>> import numpy as np
        >>> from rclpy.clock import ROSClock
        >>> arr = np.array([[1, 2], [3, 4]])
        >>> msg = to_ros2_msg(arr, timestamp=ROSClock().now(), frame_id="some_ndarray")
    """
    if timestamp is None:
        timestamp = get_now_time()
    msg = NDArray()
    header = Header()
    header.stamp = timestamp.to_msg()
    header.frame_id = frame_id
    msg.header = header
    msg.dtype = array.dtype.name
    msg.shape = array.shape
    msg.data_size = array.size
    msg.data = array.tobytes()
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
    array = np.frombuffer(msg.data, dtype=np.dtype(msg.dtype))
    return array.reshape(msg.shape)
