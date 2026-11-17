---
id: computing-software.robotics-software.robot-perception-slam.pointcloud2-handling
name: pointcloud2-handling
category: computing-software
field: robotics-software
product: robot-perception-slam
tags: [pointcloud2, sensor-msgs-py, point-cloud2-read-points, pcl-conversions, voxel-grid, organized-cloud, perception-pointcloud]
level: practitioner
status: docs-checked
description: "Read and build PointCloud2 messages in Python and C++ and filter clouds with PCL (voxel grid, passthrough, outliers)."
sources:
  - https://github.com/ros2/common_interfaces/blob/rolling/sensor_msgs/msg/PointCloud2.msg
  - https://github.com/ros2/common_interfaces/blob/rolling/sensor_msgs_py/sensor_msgs_py/point_cloud2.py
  - https://github.com/ros2/geometry2/blob/rolling/tf2_sensor_msgs/tf2_sensor_msgs/tf2_sensor_msgs.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PointCloud2 handling
```python
from sensor_msgs_py import point_cloud2
pts = point_cloud2.read_points(msg, field_names=['x', 'y', 'z'], skip_nans=True)   # structured numpy array
xyz = point_cloud2.read_points_numpy(msg, field_names=['x', 'y', 'z'], skip_nans=True)   # plain (N, 3) array
out = point_cloud2.create_cloud_xyz32(msg.header, xyz)   # PointCloud2 with x, y, z float32 fields
```
- `sensor_msgs_py.point_cloud2` provides `read_points(cloud, field_names=None, skip_nans=False, uvs=None, reshape_organized_cloud=False)`, `read_points_numpy` (same arguments, for equally typed fields), `read_points_list` and `create_cloud_xyz32(header, points)`.
- Message layout: `height` is 1 and `width` is the point count for an unordered cloud; `point_step` is the length of a point in bytes; `data` has `row_step * height` bytes; `is_dense` is true if there are no invalid points.
- To transform a cloud into another frame in Python, use `do_transform_cloud` from `tf2_sensor_msgs.tf2_sensor_msgs` with a `TransformStamped` from a tf2 buffer lookup.
- Keep the source `header` (stamp and `frame_id`) on any cloud you publish derived from another.

## Gotchas
- Use `skip_nans=True` when NaN points would break later maths.
- `read_points` returns a structured array; use `read_points_numpy` when you want a plain 2D array (all requested fields must have the same type).

## Self-check
The cloud displays in RViz in the expected frame with sensible extents.

## Checked
2026-11-03. Confirmed in PointCloud2.msg (field comments) and `sensor_msgs_py/point_cloud2.py` (function names, signatures, `create_cloud_xyz32`) and tf2_sensor_msgs.py (`do_transform_cloud`). Removed: PCL C++ conversion and filter claims (VoxelGrid, fromROSMsg), the downsampling-before-processing advice, organized-cloud cost claims and intra-process publishing advice.
Method: documentation only; no commands were run.
