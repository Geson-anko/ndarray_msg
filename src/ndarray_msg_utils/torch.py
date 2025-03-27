import ctypes

import torch
from numpy_ndarray_msgs.msg import NDArray
from rclpy.time import Time
from std_msgs.msg import Header

from .utils import get_now_time

__all__ = [
    "to_ros_msg",
    "from_ros_msg",
    "NDArray",
]


def tensor_to_buffer(tensor: torch.Tensor) -> bytes:
    """Convert PyTorch tensor to bytes buffer.

    Converts tensor to CPU if on another device, then creates a bytes buffer
    from the tensor's memory.

    Args:
        tensor: Input PyTorch tensor

    Returns:
        Bytes buffer containing tensor data
    """
    if tensor.device.type != "cpu":
        tensor = tensor.cpu()
    nbytes = tensor.nelement() * tensor.element_size()
    ptr = tensor.data_ptr()
    return ctypes.string_at(ptr, nbytes)


def buffer_to_tensor(
    buffer: bytes, shape: tuple[int, ...], dtype: torch.dtype
) -> torch.Tensor:
    """Convert bytes buffer back to PyTorch tensor.

    Reconstructs a PyTorch tensor from a bytes buffer with specified shape and dtype.

    Args:
        buffer: Input bytes containing tensor data
        shape: Shape of the tensor to reconstruct
        dtype: Data type of the tensor

    Returns:
        Reconstructed PyTorch tensor
    """
    return torch.frombuffer(bytearray(buffer), dtype=dtype).reshape(shape)


def to_ros_msg(
    tensor: torch.Tensor,
    timestamp: Time | None = None,
    frame_id: str = "",
) -> NDArray:
    """Convert PyTorch tensor to ROS2 NDArray message.

    Creates a ROS2 NDArray message containing the serialized tensor data.
    Includes header with timestamp and frame_id.

    Args:
        tensor: Input PyTorch tensor
        timestamp: ROS Time object for header. Uses current time if None
        frame_id: Frame ID string for header

    Returns:
        ROS2 NDArray message containing the serialized tensor
    """
    if timestamp is None:
        timestamp = get_now_time()
    msg = NDArray()
    header = Header()
    header.stamp = timestamp.to_msg()
    header.frame_id = frame_id
    msg.header = header
    msg.dtype = str(tensor.dtype)
    msg.shape = tuple(tensor.shape)
    msg.data_size = tensor.nelement()
    msg.data = tensor_to_buffer(tensor)
    return msg


def from_ros_msg(msg: NDArray) -> torch.Tensor:
    """Convert ROS2 NDArray message back to PyTorch tensor.

    Reconstructs original PyTorch tensor from NDArray message by deserializing
    the binary data using stored dtype and shape information.

    Args:
        msg: Input ROS2 NDArray message

    Returns:
        Reconstructed PyTorch tensor

    Raises:
        ValueError: If dtype string is invalid or not a torch dtype
    """
    if not msg.dtype.startswith("torch."):
        raise ValueError("Message dtype must start with 'torch.'")
    dtype_str = msg.dtype.split(".")[-1]
    dtype = getattr(torch, dtype_str)
    if not isinstance(dtype, torch.dtype):
        raise ValueError(f"Invalid torch dtype: {dtype_str}")
    tensor = buffer_to_tensor(msg.data, tuple(msg.shape), dtype)
    return tensor
