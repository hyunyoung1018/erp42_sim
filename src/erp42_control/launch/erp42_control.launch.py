from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    ackermann_steering_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["ackermann_steering_controller", "--controller-manager", "/controller_manager"],
    )

    return LaunchDescription([
        joint_state_broadcaster_spawner,
        ackermann_steering_controller_spawner
    ])