---
id: computing-software.robotics-software.ros2-core.tf2-broadcast
name: tf2-broadcast
category: computing-software
field: robotics-software
product: ros2-core
tags: [tf2-broadcast, transform-broadcaster, static-transform-broadcaster, transform-stamped, tf-frames, ros2-tf2]
level: practitioner
status: docs-checked
description: "Publish dynamic and static transforms with tf2_ros TransformBroadcaster and StaticTransformBroadcaster."
sources:
  - https://github.com/ros2/ros2_documentation
  - https://www.ros.org/reps/rep-0105.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tf2 broadcasting
```python
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
t = TransformStamped()
t.header.stamp = self.get_clock().now().to_msg()
t.header.frame_id = 'odom'; t.child_frame_id = 'base_link'
t.transform.translation.x = x; t.transform.rotation.w = 1.0   # identity rotation
TransformBroadcaster(self).sendTransform(t)
```
- Static transforms are published on `/tf_static` (`ros2 topic echo /tf_static` shows them).
- REP 105 uses a tree: each frame has exactly one parent and any number of children.
- Convention (REP 105): `map -> odom -> base_link -> sensors`.
- Static from CLI: `ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 0.1 --frame-id base_link --child-frame-id lidar`; every option except `--frame-id` and `--child-frame-id` is optional (identity assumed), and rotation can be given as `--yaw --pitch --roll` or `--qx --qy --qz --qw`.

## Gotchas
- Use `rotation.w = 1.0` for no rotation rather than leaving all components zero.

## Self-check
`ros2 run tf2_tools view_frames` produces a diagram of the frames being broadcast.

## Checked
2026-11-03. Confirmed in ros2_documentation tf2 tutorials (static broadcaster pages: `StaticTransformBroadcaster`, `/tf_static`, `static_transform_publisher` flags and optional-argument rule; Introduction-To-Tf2: `view_frames`) and REP 105 (tree, map -> odom -> base_link). Removed: transient-local claim, older positional syntax, normalisation and two-publisher claims, "PDF" detail.
Method: documentation only; no commands were run.
