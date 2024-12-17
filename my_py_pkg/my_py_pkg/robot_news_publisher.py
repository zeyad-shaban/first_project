import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class RobotNewsPublisher(Node):
    def __init__(self):
        super().__init__('robot_news_publisher')
        self.declare_parameter('robot_name', 'X001')
        self.declare_parameter('publish_freq', 2)

        self.robot_name = self.get_parameter('robot_name').value
        publish_freq = self.get_parameter('publish_freq').value


        self.publisher_ = self.create_publisher(String, 'robot_news', 10)
        self.timer_ = self.create_timer(1/publish_freq, self.publish_news)

        self.get_logger().info('Started robot_news publisher')

    def publish_news(self):
        msg = String()
        msg.data = f"hello, {self.robot_name} is ready to take over!"

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = RobotNewsPublisher()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
