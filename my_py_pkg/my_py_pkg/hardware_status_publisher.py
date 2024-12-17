import rclpy
from rclpy.node import Node
from dummy_interfaces.msg import HardwareStatus


class HardwareStatusPublisher(Node):
    def __init__(self):
        super().__init__('hardware_status_publisher')

        self.send_hw_status_timer = self.create_timer(1, self.send_hardware_status)
        self.hw_status_publisher = self.create_publisher(HardwareStatus, 'hardware_status', 10)

        self.get_logger().info('hardware_status Topic Started...')

    def send_hardware_status(self):
        msg = HardwareStatus(temprature=10, are_motors_ready=True, debug_msg='hogla bogla', burning=True)
        self.hw_status_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = HardwareStatusPublisher()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
