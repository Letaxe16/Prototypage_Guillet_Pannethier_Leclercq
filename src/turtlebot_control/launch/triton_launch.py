from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlebot_control',
            executable='turtlebot_control',
        ),
        Node(
            package='joy',
            executable='joy_node',
        )
    ])