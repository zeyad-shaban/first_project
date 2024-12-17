import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')

        self.call_add_two_ints_server(5, 6)
        self.get_logger().info('add_two_ints_client Started...')

    def call_add_two_ints_server(self, a, b):
        client_ = self.create_client(AddTwoInts, 'add_two_ints')
        while not client_.wait_for_service(1.0):
            self.get_logger().warning('Waiting for service...')

        req = AddTwoInts.Request()
        req.a = a
        req.b = b

        future = client_.call_async(req)
        future.add_done_callback(lambda future: self.callback_future_add_two_ints(future, req))

    def callback_future_add_two_ints(self, future, req):
        try:
            res = future.result()
            self.get_logger().info(f"{req.a} + {req.b} = {res.sum}")
        except Exception as e:
            self.get_logger().error(f"add_two_ints_client service call failed: %r", (e,))


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClient()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()