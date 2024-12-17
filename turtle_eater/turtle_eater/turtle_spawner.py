import random

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from turtle_eater_interfaces.msg import TurtlePosition, TurtlePositionArray
from example_interfaces.msg import String


class TurtleSpawner(Node):
    turtle_positions = TurtlePositionArray()

    def __init__(self):
        super().__init__("turtle_spawner")

        self.declare_parameter("spawn_freq", 0.5)
        self.declare_parameter("turtles_pos_publish_freq", 10)

        spawn_freq = self.get_parameter('spawn_freq').value
        turtles_pos_publish_freq = self.get_parameter('turtles_pos_publish_freq').value

        self.spawn_timer = self.create_timer(1 / spawn_freq, self.spawn_turtle)
        self.turtles_pos_timer = self.create_timer(1 / turtles_pos_publish_freq, self.publish_turtles_pos)

        # Subscribers
        self.remove_turtle_pos_subscriber = self.create_subscription(String, 'remove_turtle_pos',
                                                                     self.callback_remove_turtle_pos, 10)

        # Clients
        self.spawn_client = self.create_client(Spawn, 'spawn')

        # Services
        self.turtle_positions_publisher = self.create_publisher(TurtlePositionArray, "turtle_positions", 10)

        # Wait
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Service not available, waiting again...')

        self.get_logger().info('turtle_spawner started')

    def publish_turtles_pos(self):
        self.turtle_positions_publisher.publish(self.turtle_positions)

    def spawn_turtle(self):
        pos = self.get_random_position()
        req = Spawn.Request(x=pos.x, y=pos.y)

        future = self.spawn_client.call_async(req)
        future.add_done_callback(lambda fut: self.add_position_callback(fut, pos))

    def add_position_callback(self, fut, pos: TurtlePosition):
        pos.name = fut.result().name
        self.turtle_positions.positions.append(pos)

    def get_random_position(self) -> TurtlePosition:
        pos = TurtlePosition()
        pos.x = random.random() * 11
        pos.y = random.random() * 11
        return pos

    def callback_remove_turtle_pos(self, name: String):
        name = name.data

        self.get_logger().warning(f'WILL Remove turtle pos {name}, length: {len(self.turtle_positions.positions)}')
        for pos in self.turtle_positions.positions:
            if pos.name == name:
                self.turtle_positions.positions.remove(pos)
        self.get_logger().warning(f'Removed turtle pos {name}, length: {len(self.turtle_positions.positions)}')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawner()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
