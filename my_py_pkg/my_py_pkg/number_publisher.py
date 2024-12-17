import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool


class NumberPublisher(Node):
    def __init__(self):
        super().__init__('number_publisher')
        self.declare_parameter('publish_frequency', 3.0)
        self.declare_parameter('val_to_publish', 1)

        publish_frequency = self.get_parameter('publish_frequency').value
        self.val_to_publish = self.get_parameter('val_to_publish').value

        self.publisher_ = self.create_publisher(Int64, 'number', 10)
        self.timer_ = self.create_timer(1/publish_frequency, self.callback_publish_number)
        self.client_ = self.create_client(SetBool, 'reset_counter')

        while not self.client_.wait_for_service(1.0):
            self.get_logger().warning('service reset_counter not available...')

        self.get_logger().info('number_publisher Started...')

        self.reset_counter()

    def callback_publish_number(self):
        msg = Int64()
        msg.data = self.val_to_publish
        self.publisher_.publish(msg)

    def reset_counter(self):
        req = SetBool.Request()
        req.data = True
        future = self.client_.call_async(req)

        future.add_done_callback(
            lambda fut: self.get_logger().info(f"Received from reset_counter: {fut.result().success}"))


def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
