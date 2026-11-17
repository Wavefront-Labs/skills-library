---
id: computing-software.computer-graphics-engineering.computer-vision.lidar-camera-projection-and-fusion
name: lidar-camera-projection-and-fusion
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, depth-estimation, lidar-camera-fusion, extrinsic-calibration, point-projection, sensor-fusion, autonomous-driving]
level: advanced
status: verified
description: "Fuse lidar and camera data: extrinsic calibration, projecting points into images, time sync and motion compensation, colouring point clouds, and early/late fusion for detection."
sources: ["https://www.cvlibs.net/datasets/kitti/setup.php", "https://github.com/koide3/direct_visual_lidar_calibration", "https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lidar-camera projection and fusion

## Projection
```python
P_cam = (T_cam_lidar @ np.c_[pts, np.ones(len(pts))].T)[:3]      # 3 x N in camera frame
front = P_cam[2] > 0.1
uv, _ = cv2.projectPoints(P_cam[:, front].T, np.zeros(3), np.zeros(3), K, dist)
uv = uv.reshape(-1, 2); z = P_cam[2, front]
inside = (uv[:, 0] >= 0) & (uv[:, 0] < w) & (uv[:, 1] >= 0) & (uv[:, 1] < h)
```
- Drop points behind the camera before projecting.
- Build a sparse depth image: when several points hit one pixel keep the nearest (z-buffer; sort by descending z and assign, so the nearest write wins); the
  lidar sees around occluders the camera cannot (parallax), so far points leak through foreground
  edges otherwise.
- KITTI: `P2 @ R0_rect @ Tr_velo_to_cam` (rectified frame; the devkit readme gives x = P2 * R0_rect * Tr_velo_to_cam * y with R0_rect and Tr_velo_to_cam extended to 4x4).

## Extrinsic calibration
- Target-based: checkerboard/ArUco boards with holes or planar boards; correspond board planes/edges
  in both sensors.
- Targetless: mutual-information or edge alignment (e.g. `direct_visual_lidar_calibration`).
- Validate by overlaying projected points on edges (poles, building corners) at several distances;
  0.5 degree rotation error = 8.7 cm at 10 m (10 m x tan 0.5 degrees).

## Time and motion
- Spinning lidar sweeps take about 100 ms (KITTI: 10 Hz, cameras triggered by the Velodyne) while a camera exposes in milliseconds: compensate points to
  the camera timestamp using ego-motion (deskew), or trigger the camera when the lidar beam passes
  its FOV.
- Rolling shutter cameras add row-dependent time offsets.

## Fusion strategies
- **Colour the cloud**: sample image colour at projected points (with occlusion check).
- **Early fusion**: lidar depth as extra image channels, or painted points (PointPainting:
  segmentation scores attached to points).
- **Late fusion**: detect in each sensor, associate in 3D/BEV.
- **BEV fusion**: lift image features to bird's-eye view (BEVFusion) and concatenate with lidar
  BEV features.

## Verify
Overlay video of projected points colour-coded by depth: edges must stay aligned while driving and
turning (catches time-offset errors as well as extrinsic errors).

## Checked
OpenCV 5.0.0, NumPy 2.5.4.
- Run: the projection snippet on 2,000 synthetic points (behind-camera filter, `projectPoints`, in-image mask 769 points, nearest-wins z-buffer 768 filled pixels).
- Fetched: KITTI object devkit readme (projection formula, 4x4 extension note), KITTI raw-data readme (about 10 Hz, cameras triggered by the Velodyne); arXiv titles for PointPainting (1911.10150) and BEVFusion (2205.13542); direct_visual_lidar_calibration repository exists (HTTP 200).
