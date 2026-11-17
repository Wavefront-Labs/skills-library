---
id: computing-software.robotics-software.ros2-core.composable-nodes
name: composable-nodes
category: computing-software
field: robotics-software
product: ros2-core
tags: [composable-nodes, component-container, rclcpp-components, load-component, composablenode, ros2-composition]
level: advanced
status: docs-checked
description: "Build rclcpp components and load them into a container to share a process."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/nodes/Working-with-nodes/Composition.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/nodes/Working-with-nodes/Writing-a-Composable-Node.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Launch/Launching-composable-nodes.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Composable nodes
A component class registers itself with macros from `rclcpp_components` (`rclcpp_components_register_node` or `rclcpp_components_register_nodes` in CMake); see Writing-a-Composable-Node for the exact call. The node constructor takes a `NodeOptions` argument.

Run: `ros2 run rclcpp_components component_container`, then `ros2 component load /ComponentManager <package> <plugin_class>` (the tutorial uses `composition composition::Talker`); `ros2 component list` and `ros2 component types` show what is loaded and available.
- Launch: `ComposableNode(...)` entries in a container, or `LoadComposableNodes` to load components into a given container.
- Benefit: composing nodes in one process can reduce overhead and simplify deployment.

## Gotchas
- Use `extra_arguments=[{'use_intra_process_comms': True}]` to enable intra-process communication.

## Checked
2026-11-02. Confirmed in Composition, Writing-a-Composable-Node and Launching-composable-nodes (ros2_documentation, rolling): component_container, ros2 component load/list/types, NodeOptions constructor, registration macros, ComposableNode, LoadComposableNodes, use_intra_process_comms extra argument. Removed the CMake example (PLUGIN/EXECUTABLE arguments and ament_target_dependencies not shown), the Nav2 claim and the crash claim.
Method: documentation only; no commands were run.

## Self-check
`ros2 component list` shows the loaded component and its node in `ros2 node list`.
