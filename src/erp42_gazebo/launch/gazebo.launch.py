import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    description_pkg_path = get_package_share_directory('erp42_description')
    
    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=[os.path.join(description_pkg_path, '..')]
    )

    description_share = FindPackageShare('erp42_description')
    gazebo_share = FindPackageShare('erp42_gazebo')
    gazebo_ros_share = FindPackageShare('gazebo_ros')
    
    default_model_path = PathJoinSubstitution([description_share, 'urdf', 'erp42.urdf.xacro'])
    world_path = PathJoinSubstitution([gazebo_share, 'worlds', 'empty.world'])
    
    # 1. Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', default_model_path]), 'use_sim_time': True}]
    )

    # 2. Gazebo Server (verbose 켜기)
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([gazebo_ros_share, 'launch', 'gzserver.launch.py'])),
        launch_arguments={'world': world_path, 'pause': 'false', 'verbose': 'false'}.items()
    )
    
    # 3. Gazebo Client
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([gazebo_ros_share, 'launch', 'gzclient.launch.py']))
    )

    # 4. Spawn Entity
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'erp42'],
        output='screen'
    )

    # 5. Joint State Broadcaster (타이머 추가로 안정성 확보)
    load_joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    # 6. Ackermann Steering Controller
    load_ackermann_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["ackermann_steering_controller", "--controller-manager", "/controller_manager"],
    )

    return LaunchDescription([
        set_gazebo_model_path,
        robot_state_publisher_node,
        gazebo_server,
        gazebo_client,
        spawn_entity,
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_joint_state_broadcaster],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_broadcaster,
                on_exit=[load_ackermann_controller],
            )
        ),
    ])