from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    hunter_name = 'turtle1'

    ld.add_action(Node(
        package='turtlesim',
        executable='turtlesim_node',
        name=hunter_name,
    ))

    ld.add_action(Node(
        package='turtle_eater',
        executable='turtle_hunter',
        parameters=[
            {'hunter_name': hunter_name}
        ]
    ))

    ld.add_action(Node(
        package='turtle_eater',
        executable='turtle_spawner',
        parameters=[
            {"spawn_freq": 0.5},
            {"turtles_pos_publish_freq": 10}
        ]
    ))

    return ld
