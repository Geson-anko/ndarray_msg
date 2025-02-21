from collections.abc import Generator

import numpy as np
import pytest
import rclpy
from ndarray_msg.msg import NDArray
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.publisher import Publisher
from rclpy.subscription import Subscription

from ndarray_msg_utils.conversion import from_ros_msg, to_ros_msg


class TestPublisher(Node):
    """Test publisher node for NDArray messages."""

    def __init__(self, topic_name: str = "test_topic", qos_depth: int = 10) -> None:
        super().__init__("test_publisher")
        self._publisher: Publisher = self.create_publisher(
            NDArray, topic_name, qos_depth
        )
        self._counter = 0

    def publish_test_array(self) -> None:
        array = np.array(
            [
                [self._counter, self._counter + 1],
                [self._counter + 2, self._counter + 3],
            ],
            dtype=np.float32,
        )
        msg = to_ros_msg(array)
        self._publisher.publish(msg)
        self._counter += 1


class TestSubscriber(Node):
    """Test subscriber node for NDArray messages."""

    def __init__(self, topic_name: str = "test_topic", qos_depth: int = 10) -> None:
        super().__init__("test_subscriber")
        self._subscription: Subscription = self.create_subscription(
            NDArray, topic_name, self._message_callback, qos_depth
        )
        self.last_array: np.ndarray | None = None
        self.received_count = 0

    def _message_callback(self, msg: NDArray) -> None:
        self.last_array = from_ros_msg(msg)
        self.received_count += 1


@pytest.fixture(scope="session")
def rclpy_init() -> Generator[None, None, None]:
    rclpy.init()
    yield
    rclpy.shutdown()


@pytest.fixture
def executor(rclpy_init) -> SingleThreadedExecutor:
    return SingleThreadedExecutor()


@pytest.fixture
def publisher_node(executor: SingleThreadedExecutor) -> TestPublisher:
    node = TestPublisher()
    executor.add_node(node)
    return node


@pytest.fixture
def subscriber_node(executor: SingleThreadedExecutor) -> TestSubscriber:
    node = TestSubscriber()
    executor.add_node(node)
    return node


def test_ndarray_communication(
    executor: SingleThreadedExecutor,
    publisher_node: TestPublisher,
    subscriber_node: TestSubscriber,
) -> None:
    """Test NDArray message communication between nodes."""
    # Initial state check
    assert subscriber_node.last_array is None
    assert subscriber_node.received_count == 0

    # Publish test data
    publisher_node.publish_test_array()

    # Allow time for message processing
    executor.spin_once(timeout_sec=1.0)

    # Verify message reception
    assert subscriber_node.received_count == 1
    assert subscriber_node.last_array is not None
    assert subscriber_node.last_array.shape == (2, 2)
    assert subscriber_node.last_array.dtype == np.float32

    # Verify array content
    expected_value = publisher_node._counter - 1
    np.testing.assert_array_equal(
        subscriber_node.last_array,
        np.array(
            [
                [expected_value, expected_value + 1],
                [expected_value + 2, expected_value + 3],
            ],
            dtype=np.float32,
        ),
    )

    # Test multiple messages
    publisher_node.publish_test_array()
    executor.spin_once(timeout_sec=1.0)
    assert subscriber_node.received_count == 2

    # Cleanup
    executor.remove_node(publisher_node)
    executor.remove_node(subscriber_node)
