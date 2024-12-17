from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    
    remap_number_topic = ("number_count", "number_count_bruh")
    
    number_publisher = Node(
        package="my_py_pkg",
        executable="number_publisher",
        remappings=[
            remap_number_topic
        ],
        parameters=[
            {"val_to_publish": 1000000},
            {'publish_frequency':  1000.0  }
        ]
    )
    
    number_counter = Node(
        package="my_cpp_pkg",
        executable="number_counter",
        remappings=[
            remap_number_topic
        ],
        parameters=[
            {'initial_value': 0}
        ]
    )

    ld.add_action(number_publisher)
    ld.add_action(number_counter)
    
    return ld