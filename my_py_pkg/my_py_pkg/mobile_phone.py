import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MobilePhone(Node):
    def __init__(self):
        super().__init__('mobile_phone')

        self.subscription_ = self.create_subscription(String, 'robot_news', self.on_robot_news, 10)
        self.get_logger().info('mobile_phone started')

    def on_robot_news(self, msg):
        self.get_logger().info(f'data received: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = MobilePhone()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
