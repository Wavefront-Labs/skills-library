---
id: computing-software.robotics-software.ros2-navigation-nav2.bt-navigator-xml
name: bt-navigator-xml
category: computing-software
field: robotics-software
product: ros2-navigation-nav2
tags: [bt-navigator, behavior-tree-xml, navigate-to-pose-bt, recovery-node, rate-controller, bt-plugins, nav2-behavior-trees]
level: advanced
status: docs-checked
description: "Customize the BT Navigator: pick a behavior tree XML, add nodes and replan or recovery logic."
sources:
  - https://docs.nav2.org/
  - https://github.com/ros-navigation/docs.nav2.org
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BT Navigator
```yaml
bt_navigator:
  ros__parameters:
    default_nav_to_pose_bt_xml: /abs/path/navigate_to_pose_w_replanning_and_recovery.xml
    # plugin_lib_names: []   # all Nav2 BT libraries load automatically; list only your custom ones
```
```xml
<root BTCPP_format="4"><BehaviorTree ID="MainTree">
  <RecoveryNode number_of_retries="6">
    <PipelineSequence name="Nav">
      <RateController hz="1.0"><ComputePathToPose goal="{goal}" path="{path}" planner_id="GridBased"/></RateController>
      <FollowPath path="{path}" controller_id="FollowPath"/>
    </PipelineSequence>
    <ReactiveFallback name="Recovery"><GoalUpdated/><Sequence><ClearEntireCostmap service_name="local_costmap/clear_entirely_local_costmap"/><Spin spin_dist="1.57"/></Sequence></ReactiveFallback>
  </RecoveryNode>
</BehaviorTree></root>
```
- Nav2 uses BehaviorTree.CPP; default trees ship in `nav2_bt_navigator/behavior_trees`. Format version (3 or 4) depends on the distro.
- All Nav2 BT node libraries are included automatically; `plugin_lib_names` only needs your custom plugins. Per-request trees via the goal's `behavior_tree` field.

## Gotchas
- A custom node whose library is not in `plugin_lib_names` fails at XML load.
- Blackboard variable names are case-sensitive.

## Self-check
Blocking the path triggers replanning and a recovery in the logs.

## Checked
2026-11-03: parameter, plugin, API and command names compared with the Nav2 documentation sources (docs.nav2.org repository): core-server configuration pages (AMCL, BT Navigator, behavior, planner, smoother, docking, map saver, waypoint follower, costmap), the Simple Commander API page, the docking tutorial and the Jazzy and Lyrical migration guides. Removed or corrected: the hand-listed BT plugin libraries (all Nav2 BT libraries load automatically per the bt_navigator page).

Method: documentation only; no commands were run.
