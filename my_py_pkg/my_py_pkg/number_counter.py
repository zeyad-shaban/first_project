import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool


class NumberCounter(Node):
    def __init__(self):
        super().__init__('number_counter')

        self.count_ = 0
        self.publisher_number_count_ = self.create_publisher(Int64, 'number_count', 10)
        self.subscriber_number = self.create_subscription(Int64, 'number', self.callback_number_count, 10)
        self.service_ = self.create_service(SetBool, 'reset_counter', self.callback_reset_counter)

        self.get_logger().info('number_counter Started...')

    def callback_reset_counter(self, req: SetBool.Request, res: SetBool.Response) -> SetBool.Response:
        if req.data:
            self.count_ = 0

        self.get_logger().info('number_counter Reset...')
        res.success = True
        return res


    def callback_number_count(self, msg: Int64):
        res = Int64()

        self.count_ += msg.data
        res.data = self.count_

        self.publisher_number_count_.publish(res)


def main(args=None):
    rclpy.init(args=args)
    node = NumberCounter()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
