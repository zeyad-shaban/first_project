import rclpy
from rclpy.node import Node
from dummy_interfaces.srv import SetBatteryLed


class BatteryControl(Node):
    def __init__(self):
        super().__init__('battery_control')
        self.battery_percentage = 1
        self.is_consuming = True
        self.timer = self.create_timer(4, self.callback_consume_battery)
        self.client = self.create_client(SetBatteryLed, 'set_battery_led')

        self.get_logger().info('battery_control/set_battery_led is on...')


    def set_battery_led(self):
        req = SetBatteryLed.Request()
        req.battery_percentage = self.battery_percentage
        self.client.call_async(req)

    def callback_consume_battery(self):
        self.battery_percentage -= 1 / 3
        self.get_logger().info('Consumed 1/3 of battery, Battery status is {}%'.format(self.battery_percentage))

        if self.battery_percentage <= 1/3:
            self.switch_to_charging()

        self.set_battery_led()

    def callback_charge_battery(self):
        self.battery_percentage += 1 / 3
        self.get_logger().info('Charged 1/3 of battery, Battery status is {}%'.format(self.battery_percentage))

        if self.battery_percentage >= 1:
            self.switch_to_consuming()

        self.set_battery_led()

    def switch_to_charging(self):
        self.timer.cancel()
        self.is_consuming = False
        self.timer = self.create_timer(6, self.callback_charge_battery)
        self.get_logger().info('Switched to charging mode...')

    def switch_to_consuming(self):
        self.timer.cancel()
        self.is_consuming = True
        self.timer = self.create_timer(4, self.callback_consume_battery)

        self.get_logger().info('Switched to consuming mode...')


def main(args=None):
    rclpy.init(args=args)
    node = BatteryControl()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
