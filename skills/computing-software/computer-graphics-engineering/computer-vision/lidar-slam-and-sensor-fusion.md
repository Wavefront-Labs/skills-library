---
id: computing-software.computer-graphics-engineering.computer-vision.lidar-slam-and-sensor-fusion
name: lidar-slam-and-sensor-fusion
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, sfm-slam, lidar-slam, lidar-inertial-odometry, kiss-icp, fast-lio, sensor-fusion]
level: advanced
status: draft
description: "Run lidar SLAM: KISS-ICP odometry, LIO-SAM/FAST-LIO2 lidar-inertial fusion, deskewing, IMU-lidar extrinsics and time sync, loop closure and map export."
sources: ["https://github.com/PRBonn/kiss-icp", "https://github.com/TixiaoShan/LIO-SAM", "https://github.com/hku-mars/FAST_LIO", "https://arxiv.org/abs/2209.15397"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lidar SLAM and sensor fusion

## Options
| System | Inputs | Notes |
|---|---|---|
| KISS-ICP | Lidar only | Point-to-point ICP, adaptive threshold, minimal tuning; good baseline |
| FAST-LIO2 | Lidar + IMU | Iterated EKF, ikd-tree, very fast, robust to aggressive motion |
| LIO-SAM | Lidar + IMU (+GPS) | Factor graph (GTSAM), loop closure, GPS factors |
| Cartographer | 2D/3D lidar | Submaps, widely used for 2D indoor robots |

```bash
pip install kiss-icp
kiss_icp_pipeline --visualize /data/sequence.bag      # rosbag, PCD folder, KITTI, ...
```

## Must-haves
- **Deskewing**: spinning lidars capture a sweep over about 100 ms; with motion, points must be
  corrected with per-point timestamps and IMU/constant-velocity motion. Missing per-point time
  fields (`t`/`time` in the PointCloud2) silently disable this.
- **Extrinsics** IMU-lidar: rotation must be accurate (degrees matter); LIO-SAM needs the IMU
  frame convention set in its params. Calibrate with tools like LI-Init or from CAD plus
  refinement.
- **Time sync**: hardware PTP/PPS where possible; a 10 ms offset at 1 m/s and fast rotation
  produces blurred maps.
- IMU noise parameters from Allan variance, not guessed.

## Degeneracy
Long corridors, tunnels, open fields: ICP is unconstrained along some axes. Detect via the
eigenvalues of the ICP Hessian; fuse wheel odometry/IMU or add constraints.

## Loop closure and maps
Scan Context or similar descriptors for place recognition, ICP for the relative pose, pose-graph
optimisation. Export maps as PCD/PLY, voxel-downsample, and build occupancy grids for navigation.

## Evaluate
ATE/RPE with `evo` against GNSS-INS ground truth (KITTI, Newer College, Hilti datasets).
