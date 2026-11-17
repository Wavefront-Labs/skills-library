---
id: computing-software.robotics-software.robot-perception-slam.slam-toolbox-localization
name: slam-toolbox-localization
category: computing-software
field: robotics-software
product: robot-perception-slam
tags: [slam-localization, localization-mode, lifelong-mapping, pose-graph, map-file-name, nav2-slam-launch]
level: advanced
status: docs-checked
description: "Localize on a serialized slam_toolbox map and use lifelong mapping; integrate with Nav2."
sources:
  - https://github.com/SteveMacenski/slam_toolbox/blob/ros2/README.md
  - https://github.com/SteveMacenski/slam_toolbox/blob/ros2/config/mapper_params_localization.yaml
  - https://github.com/SteveMacenski/slam_toolbox/blob/ros2/srv/DeserializePoseGraph.srv
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# slam_toolbox localization
```yaml
slam_toolbox:
  ros__parameters:
    mode: localization
    map_file_name: /path/lab            # serialized pose-graph file (from serialize_map)
    map_start_pose: [0.0, 0.0, 0.0]     # or map_start_at_dock: true
```
```bash
ros2 launch slam_toolbox localization_launch.py slam_params_file:=/path/mapper_params_localization.yaml
```
- Localization needs a serialized pose graph (saved with `/slam_toolbox/serialize_map`), not just a map image. `map_file_name` is the pose-graph file to load on startup.
- `map_start_pose` sets the pose to start in; `map_start_at_dock` starts at the first node of the graph. If both are set, the pose is used.
- `mode: localization` lets the solver add and remove nodes and constraints quickly; the README says it is a performance optimisation and not strictly required. The approach is called elastic pose-graph localization: it localizes within the existing pose graph using a rolling window of recent scans.
- The node subscribes to `/initialpose` (the AMCL topic), so RViz 2D Pose Estimate can relocalize it.
- `/slam_toolbox/deserialize_map` (`DeserializePoseGraph`) loads a pose graph at runtime with a `filename`, a `match_type` (`START_AT_FIRST_NODE` 1, `START_AT_GIVEN_POSE` 2, `LOCALIZE_AT_POSE` 3) and an `initial_pose` (map to base frame).
- `scan_buffer_size` is the size of the circular buffer of scans used in localization mode. The package also provides `lifelong_launch.py` for lifelong mapping (update and re-serialize an existing map).

## Gotchas
- The example `mapper_params_localization.yaml` shows `mode: mapping #localization`; set `mode: localization` yourself.
- Files serialized before 23 March 2021 may need conversion (see the README section on serialized files).

## Self-check
After launch the robot pose in RViz matches reality and stays aligned as it drives through the mapped area.

## Checked
2026-11-03. Confirmed in the slam_toolbox README (localization mode description, `/initialpose`, parameters, services, lifelong mapping), `mapper_params_localization.yaml` and `DeserializePoseGraph.srv`. Removed: Nav2 launch file claims, the claim that it is lighter than AMCL, the file-name-without-extension claim and the moving-furniture advice.
Method: documentation only; no commands were run.
