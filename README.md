# ERP42 ROS2 Gazebo Simulation

## Environment
* OS: Ubuntu 22.04 LTS
* ROS Version: ROS2 Humble
* Simulator: Gazebo 11 (Classic)

## Directory Structure

```text
erp42_sim/
└── src/
    ├── erp42_control/
    │   ├── config/
    │   │   └── erp42_controllers.yaml      # Ackermann controller and joint parameter configurations
    │   ├── launch/
    │   │   └── erp42_control.launch.py     # Launch file for loading controllers
    │   ├── CMakeLists.txt
    │   └── package.xml
    │
    ├── erp42_description/
    │   ├── launch/
    │   │   └── display.launch.py           # Launch file for Rviz2 visualization
    │   ├── meshes/                         # 3D model files (.dae)
    │   │   └── caucho.dae
    │   │   └── ...
    │   ├── rviz/
    │   │   └── erp42_display.rviz          # Rviz2 config
    │   ├── urdf/
    │   │   ├── erp42.urdf.xacro            # Top-level URDF file
    │   │   ├── erp42_core.xacro            # Definitions of physical links, joints
    │   │   ├── erp42_sensors.xacro         # Definitions of sensor links, joints
    │   │   └── erp42_gazebo.xacro          # Gazebo plugins
    │   ├── CMakeLists.txt
    │   └── package.xml
    │
    ├── erp42_gazebo/
    │   ├── launch/
    │   │   └── gazebo.launch.py            # Launch file for Gazebo, spawning the model, and loading controllers
    │   ├── modles/
    │   │   └── inu/                        # map models
    │   ├── worlds/
    │   │   └── empty.world                 # Empty Gazebo world
    │   ├── CMakeLists.txt
    │   └── package.xml
    │
    └── erp42_localization/
        ├── config/                         # Parameters for robot_localization
        │   ├── ekf_global.yaml
        │   ├── ekf_local.yaml
        │   └── navsat_transform.yaml
        ├── launch/
        │   └── localization.launch.py      # Launch file for robot_localization ekf_node, navsat_transform_node
        ├── CMakeLists.txt
        └── package.xml
```

## Prerequisites
- `ros-humble-gazebo-ros-pkgs`
- `ros-humble-ros2-control`
- `ros-humble-ros2-controllers`
- `ros-humble-gazebo-ros2-control`
- `ros-humble-ackermann-steering-controller`
- `ros-humble-joint-state-broadcaster`
- `ros-humble-teleop-twist-keyboard`

```bash
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-ros2-control ros-humble-ros2-controllers ros-humble-gazebo-ros2-control ros-humble-ackermann-steering-controller ros-humble-joint-state-broadcaster ros-humble-teleop-twist-keyboard -y
```

## Build and Launch
- Build
```bash
cd ~/erp42_sim
colcon build
source install/setup.bash
```

- Launch Gazebo and spawn the robot model
```bash
ros2 launch erp42_gazebo gazebo.launch.py
```

- Teleop Control
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/ackermann_steering_controller/reference_unstamped
```

## Acknowledgements
* The URDF structure was referenced and adapted from [nabihandres/ERP42-model](https://github.com/nabihandres/ERP42-model).
