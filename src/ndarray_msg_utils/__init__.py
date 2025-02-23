from importlib import metadata

from ndarray_msg.msg import NDArray

from .conversion import from_ros_msg, to_ros_msg

__version__ = metadata.version("ros2-ndarray-msg-utils")

__all__ = [
    "NDArray",
    "to_ros_msg",
    "from_ros_msg",
]
