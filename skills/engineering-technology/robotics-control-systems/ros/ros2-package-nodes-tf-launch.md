---
id: engineering-technology.robotics-control-systems.ros.ros2-package-nodes-tf-launch
name: ros2-package-nodes-tf-launch
category: engineering-technology
field: robotics-control-systems
product: ros
tags: [ros, ros2, ros-2, jazzy, humble, colcon, ament, ament-python, ament-cmake, rclpy, rclcpp, nodes, topics, publisher, subscriber, qos, tf2, tf2-ros, static-transform, rep-105, rep-103, launch-files, python-launch, parameters, rosdep, rqt-graph, ros2-cli, gazebo, nav2, moveit, robotics-middleware]
level: practitioner
status: docs-checked
description: "Build a ROS 2 (Jazzy/Humble) package: rclpy/rclcpp nodes, topics and QoS, tf2 frames, launch files and parameters, built with colcon and checked with ros2 CLI tools."
sources:
  - "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html"
  - "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Static-Broadcaster-Py.html"
  - "https://www.ros.org/reps/rep-0105.html"
  - "https://www.ros.org/reps/rep-0103.html"
  - "https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ROS 2 package, nodes, tf2 and launch — the core build loop

**Goal:** go from an empty workspace to a package whose nodes talk over correctly-QoS'd
topics, publish a sane tf tree, start from one launch file with parameters, and can be
inspected with the `ros2` CLI. Commands target ROS 2 **Jazzy** and **Humble**.

## 1. Workspace and package
```bash
source /opt/ros/jazzy/setup.bash          # humble: /opt/ros/humble/setup.bash
mkdir -p <WORKSPACE>/src && cd <WORKSPACE>/src
ros2 pkg create my_robot_bringup --build-type ament_python --license Apache-2.0
# then add rclpy, geometry_msgs, sensor_msgs, tf2_ros as <depend> entries in package.xml
cd <WORKSPACE>
rosdep install -i --from-path src --rosdistro jazzy -y   # pull system deps from package.xml
colcon build --symlink-install --packages-select my_robot_bringup
source install/setup.bash                  # every new shell, AFTER the /opt/ros one
```
- Use `--build-type ament_cmake` for C++ packages and `ament_python` for Python ones.
- `--symlink-install` lets you change Python files and other non-compiled resources in
  the source space without rebuilding.

## 2. A node with a timer, publisher and subscriber (rclpy)
```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, qos_profile_sensor_data
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Controller(Node):
    def __init__(self):
        super().__init__('controller')
        self.declare_parameter('rate_hz', 20.0)
        self.declare_parameter('max_speed', 0.5)
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.sub = self.create_subscription(LaserScan, 'scan', self.on_scan,
                                            qos_profile_sensor_data)
        period = 1.0 / self.get_parameter('rate_hz').value
        self.timer = self.create_timer(period, self.step)
        self.min_range = float('inf')

    def on_scan(self, msg):
        self.min_range = min((r for r in msg.ranges if r > msg.range_min), default=float('inf'))

    def step(self):
        cmd = Twist()
        cmd.linear.x = 0.0 if self.min_range < 0.4 else self.get_parameter('max_speed').value
        self.pub.publish(cmd)

def main():
    rclpy.init()
    rclpy.spin(Controller())
    rclpy.shutdown()
```
Register it in `setup.py` under `entry_points={'console_scripts': ['controller = my_robot_bringup.controller:main']}`.

**QoS gotcha (a common "no data" cause):** a subscriber asking for RELIABLE will not
match a BEST_EFFORT publisher (most sensor drivers). Use `qos_profile_sensor_data`
for sensors; use `TRANSIENT_LOCAL` durability for latched-style topics such as
`/map` or `/robot_description`. Check with `ros2 topic info -v /scan`.

## 3. tf2 frames
Follow REP-105: `map -> odom -> base_link -> sensor frames`. Exactly one node owns
each transform: localisation publishes `map->odom`, odometry/EKF publishes
`odom->base_link`, `robot_state_publisher` publishes the URDF links. Units are SI and
axes x-forward, y-left, z-up (REP-103).
```bash
ros2 run tf2_ros static_transform_publisher --x 0.2 --y 0 --z 0.15 \
  --roll 0 --pitch 0 --yaw 0 --frame-id base_link --child-frame-id laser
ros2 run tf2_ros tf2_echo base_link laser
ros2 run tf2_tools view_frames            # renders the tf tree
```
Only `--frame-id` and `--child-frame-id` are required; omitted pose arguments default to
identity. In code, look up with a `Buffer` +
`TransformListener` and `lookup_transform(target, source, rclpy.time.Time())`
(time zero = latest available); handle `TransformException` rather than crashing at start-up.

## 4. Launch file with parameters
`launch/bringup.launch.py`:
```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    sim = LaunchConfiguration('use_sim_time')
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        Node(package='my_robot_bringup', executable='controller',
             parameters=[{'use_sim_time': sim, 'rate_hz': 20.0}],
             remappings=[('cmd_vel', '/diff_drive/cmd_vel')]),
    ])
```
Install the launch folder in `setup.py` `data_files` (e.g. `('share/' + package_name + '/launch', glob('launch/*.launch.py'))`), rebuild, then
`ros2 launch my_robot_bringup bringup.launch.py use_sim_time:=true`.
Set `use_sim_time:=true` on **every** node when running a simulator that publishes `/clock`,
or tf lookups can fail with extrapolation errors.

## 5. Inspect and debug
```bash
ros2 node list ; ros2 node info /controller
ros2 topic list -t ; ros2 topic hz /scan ; ros2 topic echo /cmd_vel --once
ros2 param list /controller ; ros2 param set /controller max_speed 0.3
ros2 doctor --report ; rqt_graph
ros2 bag record -o run1 /scan /cmd_vel /tf /tf_static
```
Nodes on different machines need the same `ROS_DOMAIN_ID`.

## Verify
- [ ] `colcon build` finishes with no warnings about missing dependencies; `rosdep check` is clean.
- [ ] `ros2 topic info -v` shows compatible QoS and the expected publisher/subscriber counts.
- [ ] `ros2 topic hz` matches the designed rate.
- [ ] `view_frames` shows one connected tree with each transform owned by one node.
- [ ] The whole system starts from one `ros2 launch` command, sim time included.
- [ ] A `ros2 bag` of a run replays and reproduces the behaviour.

## Checked
2026-11-01. Confirmed against the ROS 2 Jazzy docs and REPs: `ros2 pkg create --build-type ament_python|ament_cmake --license`, `colcon build --symlink-install` and `--packages-select`, `rosdep install -i --from-path src`, `static_transform_publisher` named flags (only `--frame-id` and `--child-frame-id` required), REP-105 frame chain (map parent of odom, odom parent of base_link; odom to base_link from an odometry source, map to odom from localisation), REP-103 axes (x forward, y left, z up), QoS compatibility table (best-effort publisher with reliable subscriber does not connect), transient local for late joiners, sensor data profile uses best effort. Removed: LTS and Ubuntu version pairings, `--dependencies` usage, the discovery-range variable swap, the 5 percent rate tolerance, Nav2/MoveIt and Gazebo bridge claims. The Python and launch code samples were not run.
Method: documentation only; no commands were run.
