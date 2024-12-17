import rclpy
from rclpy.node import Node
from turtle_eater_interfaces.msg import TurtlePosition, TurtlePositionArray
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from example_interfaces.msg import String
import math

from turtlesim.srv import Kill


class TurtleHunter(Node):
    hunter_pos = Pose()

    def __init__(self):
        super().__init__("turtle_hunter")

        # Parameters
        self.declare_parameter('hunter_name', 'turtle1')
        self.declare_parameter('eating_distance', 0.3)

        hunter_name = self.get_parameter('hunter_name').value
        self.eating_distance = self.get_parameter('eating_distance').value

        # Subscribers
        self.turtle_positions_subscriber = self.create_subscription(TurtlePositionArray, 'turtle_positions',
                                                                    self.callback_turtle_hunt, 10)
        self.hunter_pos_subscriber = self.create_subscription(Pose, f'/{hunter_name}/pose',
                                                              self.callback_update_hunter_pos, 10)

        # Publishers
        self.move_hunter_publisher = self.create_publisher(Twist, f'/{hunter_name}/cmd_vel', 10)
        self.remove_turtle_pos_publisher = self.create_publisher(String, 'remove_turtle_pos', 10)

        # Services
        self.kill_client = self.create_client(Kill, '/kill')

        self.get_logger().info('turtle_hunter started')

    def callback_update_hunter_pos(self, msg: Pose):
        self.hunter_pos = msg

    def callback_turtle_hunt(self, turtle_positions: TurtlePositionArray):
        nearest_turtle_pos, min_dist = self.get_nearest_turtle(turtle_positions)

        if nearest_turtle_pos is None:
            return
        if min_dist < self.eating_distance:
            req = Kill.Request(name=nearest_turtle_pos.name)
            self.kill_client.call_async(req)
            self.remove_turtle_pos_publisher.publish(String(data=nearest_turtle_pos.name))
            return

        twist = Twist()
        linear_const = 2
        angular_const = 7

        twist.linear.x = min(min_dist * linear_const, 10.0)

        theta = math.atan2(nearest_turtle_pos.y - self.hunter_pos.y, nearest_turtle_pos.x - self.hunter_pos.x)
        theta = theta - self.hunter_pos.theta

        twist.angular.z = theta * angular_const
        self.get_logger().warning(f'Angle: {theta * angular_const}')
        self.move_hunter_publisher.publish(twist)

    def get_nearest_turtle(self, turtle_positions: TurtlePositionArray) -> (TurtlePosition, float):
        min_dist = float('inf')
        closest_turtle_position = None

        for position in turtle_positions.positions:
            dist = math.dist([self.hunter_pos.x, self.hunter_pos.y], [position.x, position.y])

            if dist < min_dist:
                min_dist = dist
                closest_turtle_position = position

        return closest_turtle_position, min_dist


def main(args=None):
    rclpy.init(args=args)
    node = TurtleHunter()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
