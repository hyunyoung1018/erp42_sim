import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('erp42_localization')
    ekf_local_config_path = os.path.join(pkg_dir, 'config', 'ekf_local.yaml')
    ekf_global_config_path = os.path.join(pkg_dir, 'config', 'ekf_global.yaml')
    navsat_config_path = os.path.join(pkg_dir, 'config', 'navsat_transform.yaml')
    
    ekf_local_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node_local',
        output='screen',
        parameters=[ekf_local_config_path, {'use_sim_time': True}],
        remappings=[('odometry/filtered', '/odometry/local')]
    )

    ekf_global_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node_global',
        output='screen',
        parameters=[ekf_global_config_path, {'use_sim_time': True}],
        remappings=[('odometry/filtered', '/odometry/global')]
    )
    
    navsat_transform_node = Node(
        package='robot_localization',
        executable='navsat_transform_node',
        name='navsat_transform_node',
        output='screen',
        parameters=[navsat_config_path, {'use_sim_time': True}],
        remappings=[
            ('imu', '/erp42/imu/data'),
            ('gps/fix', '/erp42/gps/fix'),
            ('odometry/filtered', '/odometry/global')
        ],
    )

    return LaunchDescription([
        ekf_local_node,
        ekf_global_node,
        navsat_transform_node,
    ])