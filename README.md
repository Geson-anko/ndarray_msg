[![ROS2 Humble](https://img.shields.io/badge/ROS2-Humble-blue.svg)](https://docs.ros.org/en/humble/index.html)
[![ROS2 Jazzy](https://img.shields.io/badge/ROS2-Jazzy-blue.svg)](https://docs.ros.org/en/jazzy/index.html)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Document Style](https://img.shields.io/badge/%20docstyle-google-3666d6.svg)](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings)
[![Lint & Format / Test](https://github.com/Geson-anko/numpy_ndarray_msgs/actions/workflows/main.yml/badge.svg)](https://github.com/Geson-anko/numpy_ndarray_msgs/actions/workflows/main.yml)

# ROS2 NDArray Message

A ROS2 package for transmitting NumPy ndarrays between ROS2 nodes.

## Features

- Custom ROS2 message type for numpy.ndarray
- Bi-directional conversion between NumPy arrays and ROS2 messages
- Multi-dimensional array support with various data types
- Type-safe Python utilities with full type hints

## Requirements

- ROS2 Humble or higher
- Python 3.10+

## Installation

```bash
cd ~/ros2_ws/src
git clone https://github.com/Geson-anko/numpy_ndarray_msgs.git
cd ../
colcon build --packages-select numpy_ndarray_msgs
source install/setup.sh
```

### Install Python Utility Package

```bash
pip install ros2-ndarray-msg-utils
```

## Usage

### Python Utility Package

```python
import numpy as np
from ndarray_msg_utils import to_ros_msg, from_ros_msg, NDArray
from rclpy.clock import ROSClock

# Convert NumPy array to ROS2 message
array = np.array([[1, 2], [3, 4]], dtype=np.float32)

# Type Hint
msg: NDArray

msg = to_ros_msg(array)

# with Header
msg = to_ros_msg(array, timestamp=ROSClock().now(), frame_id="array_frame")

# Convert back to NumPy array
restored = from_ros_msg(msg)
```

### PyTorch Support

```bash
pip install "ros2-ndarray-msg-utils[torch]"
```

```py
import torch
from ndarray_msg_utils.torch import to_ros_msg, from_ros_msg

# Convert PyTorch tensor to ROS2 message
tensor = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
msg = to_ros_msg(tensor)

# Convert back to PyTorch tensor
restored = from_ros_msg(msg)
```

## License

MIT License
