import pytest
import torch
from numpy_ndarray_msgs.msg import NDArray
from rclpy.time import Time

from ndarray_msg_utils.torch import (
    buffer_to_tensor,
    from_ros_msg,
    tensor_to_buffer,
    to_ros_msg,
)


@pytest.fixture
def sample_tensor():
    return torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32)


@pytest.fixture
def cuda_tensor(sample_tensor):
    if torch.cuda.is_available():
        return sample_tensor.cuda()
    pytest.skip("CUDA not available")


def test_tensor_to_buffer(sample_tensor):
    """Test conversion of tensor to bytes buffer."""
    buffer = tensor_to_buffer(sample_tensor)
    assert isinstance(buffer, bytes)
    assert len(buffer) == sample_tensor.nelement() * sample_tensor.element_size()


def test_tensor_to_buffer_cuda(cuda_tensor):
    """Test conversion of CUDA tensor to bytes buffer."""
    buffer = tensor_to_buffer(cuda_tensor)
    assert isinstance(buffer, bytes)
    assert len(buffer) == cuda_tensor.nelement() * cuda_tensor.element_size()


def test_buffer_to_tensor(sample_tensor):
    """Test reconstruction of tensor from bytes buffer."""
    buffer = tensor_to_buffer(sample_tensor)
    restored = buffer_to_tensor(buffer, sample_tensor.shape, sample_tensor.dtype)
    assert torch.equal(sample_tensor, restored)
    assert restored.dtype == sample_tensor.dtype
    assert restored.shape == sample_tensor.shape


def test_to_ros_msg(sample_tensor):
    """Test conversion of tensor to ROS message."""
    timestamp = Time(seconds=1, nanoseconds=500)
    frame_id = "test_frame"
    msg = to_ros_msg(sample_tensor, timestamp=timestamp, frame_id=frame_id)

    assert isinstance(msg, NDArray)
    assert msg.dtype == str(sample_tensor.dtype)
    assert tuple(msg.shape) == tuple(sample_tensor.shape)
    assert msg.data_size == sample_tensor.nelement()
    assert msg.header.frame_id == frame_id
    assert msg.header.stamp.sec == 1
    assert msg.header.stamp.nanosec == 500


def test_from_ros_msg(sample_tensor):
    """Test reconstruction of tensor from ROS message."""
    msg = to_ros_msg(sample_tensor)
    restored = from_ros_msg(msg)

    assert torch.equal(sample_tensor, restored)
    assert restored.dtype == sample_tensor.dtype
    assert restored.shape == sample_tensor.shape


def test_from_ros_msg_invalid_dtype():
    """Test error handling for invalid dtype in message."""
    msg = NDArray()
    msg.dtype = "invalid_dtype"
    with pytest.raises(ValueError, match="Message dtype must start with 'torch.'"):
        from_ros_msg(msg)


def test_from_ros_msg_invalid_torch_dtype():
    """Test error handling for invalid torch dtype in message."""
    msg = NDArray()
    msg.dtype = "torch.Tensor"
    with pytest.raises(ValueError, match="Invalid torch dtype"):
        from_ros_msg(msg)
