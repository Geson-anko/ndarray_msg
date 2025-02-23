from rclpy.clock import ROSClock
from rclpy.time import Time

_ROS_CLOCK = ROSClock()


def get_now_time() -> Time:
    return _ROS_CLOCK.now()
