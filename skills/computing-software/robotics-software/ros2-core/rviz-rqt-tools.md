---
id: computing-software.robotics-software.ros2-core.rviz-rqt-tools
name: rviz-rqt-tools
category: computing-software
field: robotics-software
product: ros2-core
tags: [rviz-rqt, rviz2, rqt-graph, rqt-console, rqt-plot, fixed-frame, ros2-tools-debugging]
level: practitioner
status: docs-checked
description: "Visualize with RViz 2 and inspect the graph and logs with rqt_graph and rqt_console."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Visualization/RViz/RViz-User-Guide/RViz-User-Guide.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Capabilities/Simulation/URDF/Using-URDF-with-Robot-State-Publisher-cpp.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/topics/Understanding-ROS2-Topics/Understanding-ROS2-Topics.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RViz and rqt
```bash
rviz2 -d my.rviz           # load a saved config
ros2 run rqt_graph rqt_graph   # node/topic graph
ros2 run rqt_console rqt_console   # view log messages
```
- The RViz fixed frame is the reference frame used as the world frame. It should not be moving relative to the world; it is usually `map` or `world`, but can be your odometry frame. Changing it clears the data on screen rather than re-transforming it.
- Display types include Axes, Grid, InteractiveMarker, Laser Scan, Map, Markers, Path, RobotModel and TF.
- A configuration stores the displays and their properties, tool properties, and the 3D viewpoint; `rviz2 -d <file>` loads one, as in the URDF tutorial.
- The namespace and ID of a marker together form its unique name; a new message with the same pair replaces the old marker.

## Gotchas
- A moving fixed frame (for example the robot base) makes everything the robot has seen appear in front of it.

## Self-check
RViz shows the robot model and the scan aligned in the fixed frame.

## Checked
2026-11-03. Confirmed in the RViz User Guide (fixed frame, display table, configurations), the URDF with robot_state_publisher tutorial (`rviz2 -d`), the Marker basic shapes tutorial (namespace and ID) and the ROS 2 topics tutorial (`ros2 run rqt_graph rqt_graph`) and the rqt_console tutorial (`ros2 run rqt_console rqt_console`). Removed: `rqt_reconfigure`, per-display QoS settings, the Save Config menu path, the install location for the config, `use_sim_time` advice and the "Frame does not exist" explanation.
Method: documentation only; no commands were run.
