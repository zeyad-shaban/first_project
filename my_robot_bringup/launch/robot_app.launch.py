from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    
    robot_names = ['X001', 'Giskard', 'BB8', 'Daneel', 'Jander', 'C3PO']

    for name in robot_names:
        ld.add_action(Node(
            package="my_py_pkg",
            executable=f"robot_news_publisher",
            name=f"robot_news_publisher_{name.lower()}",
            parameters= [
                {'robot_name': name}
            ]
        ))
        
    ld.add_action(Node(
        package='my_py_pkg',
        executable='mobile_phone',
        name="smartphone"
    ))
    
    return ld
    