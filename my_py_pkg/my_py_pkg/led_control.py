import rclpy
from rclpy.node import Node
from dummy_interfaces.srv import SetBatteryLed
from dummy_interfaces.msg import LedState


class LedControl(Node):
    def __init__(self):
        super().__init__('led_control')

        self.declare_parameter('led_state', [0, 0, 0])
        self.declare_parameter('publish_freq', 120)

        publish_freq = self.get_parameter('publish_freq').value
        self.leds = self.get_parameter('led_state').value

        self.server = self.create_service(SetBatteryLed, 'set_battery_led', self.callback_set_battery_led)
        self.led_state_publisher = self.create_publisher(LedState, 'led_state', 10)
        self.led_state_timer = self.create_timer(1 / publish_freq, self.publish_leds_state)

        self.get_logger().info('led_control/led_state Started...')

    def publish_leds_state(self) -> None:
        msg = LedState()
        msg.leds = self.leds
        self.led_state_publisher.publish(msg)

    def callback_set_battery_led(self, req: SetBatteryLed.Request, res: SetBatteryLed.Response):
        battery_percentage = req.battery_percentage

        if battery_percentage >= 3 / 3:
            self.leds = [0, 0, 0]
        elif battery_percentage >= 2 / 3:
            self.leds = [0, 0, 1]
        elif battery_percentage >= 1 / 3:
            self.leds = [0, 1, 1]
        else:
            self.leds = [1, 1, 1]

        response = SetBatteryLed.Response()
        response.success = True
        self.get_logger().info('leds updated: ' + str(self.leds))
        return response


def main(args=None):
    rclpy.init(args=args)
    node = LedControl()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
