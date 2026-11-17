---
id: computing-software.robotics-software.ros2-core.launch-xml-yaml
name: launch-xml-yaml
category: computing-software
field: robotics-software
product: ros2-core
tags: [launch-xml-yaml, xml-launch, yaml-launch, arg, include]
level: practitioner
status: docs-checked
description: "Write ROS 2 launch files in XML or YAML with args, includes, groups and parameters."
sources:
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Launch/Launch-file-different-formats.rst
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Launch/launch/different_formats_launch.xml
  - https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Launch/launch/different_formats_launch.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# XML and YAML launch
```xml
<launch>
  <arg name="ns" default="robot1"/>
  <node pkg="demo_nodes_cpp" exec="talker" name="talker" namespace="$(var ns)">
    <param name="use_sim_time" value="false"/>
    <remap from="chatter" to="out"/>
  </node>
  <include file="$(find-pkg-share my_pkg)/launch/other.launch.py"/>
</launch>
```
YAML equivalent: top-level `launch:` list with `- arg: {name: ns, default: robot1}` and `- node: {pkg: ..., exec: ..., name: ...}`.
- The same launch can be written in Python, XML or YAML; run any of them with `ros2 launch <package_name> <launch_file_name>`, and pass arguments as `name:=value`.
- Substitutions in the docs' example files include `$(var x)`, `$(env X)` and `$(find-pkg-share pkg)`.
- XML groups use `<group>` with `<push_ros_namespace>`; `<include file=...>` can include Python, XML and YAML launch files.

## Gotchas
- XML uses `exec`, not `type`/`executable`.
- Launch files in the three formats can include each other.

## Checked
2026-11-02. Confirmed in Launch-file-different-formats and its example XML and YAML files (ros2_documentation, rolling): arg name/default, node pkg/exec/name/namespace, param, remap, include file, $(var), $(env), $(find-pkg-share), YAML launch list with arg and node entries, cross-format includes. Removed the file-name convention and auto-detection claim, and the Python-is-easier remark (not in the docs read).
Method: documentation only; no commands were run.

## Self-check
`ros2 launch my_pkg app.launch.xml ns:=robot2` starts the node under the `robot2` namespace.
