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
git clone https://github.com/Geson-anko/ndarray_msg.git
cd ../
colcon build --packages-select ndarray_msg
source install/setup.sh
```

### Install Python Utility Package

```bash
cd ~/ros2_ws/src/ndarray_msg
pip install .
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

## License

MIT License
