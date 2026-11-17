---
id: computing-software.computer-graphics-engineering.computer-vision.visual-inertial-odometry
name: visual-inertial-odometry
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, sfm-slam, visual-inertial-odometry, vio, imu-preintegration, kalibr, openvins, orb-slam3]
level: sme
status: draft
description: "Deploy visual-inertial odometry: camera-IMU calibration with Kalibr, time sync, IMU noise parameters, filter vs optimisation VIO, initialisation, and evaluation."
sources: ["https://github.com/ethz-asl/kalibr/wiki", "https://docs.openvins.com/", "https://github.com/UZ-SLAMLab/ORB_SLAM3", "https://github.com/MichaelGrupp/evo", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Visual-inertial odometry

## 1. Why
Camera gives drift-free-ish relative structure but no metric scale (monocular) and fails in fast motion/blur;
the IMU gives metric scale, gravity direction and high-rate motion but drifts in seconds. Fused they give
metric, robust 6-DoF pose.

## 2. Calibration (non-negotiable)
1. Camera intrinsics: `kalibr_calibrate_cameras` with an AprilGrid.
2. IMU noise: record 2+ hours static, run allan_variance_ros to get gyro/accel noise density and random walk.
   Inflate them (x2-x10) in the VIO config for unmodelled effects.
3. Camera-IMU extrinsics and time offset: `kalibr_calibrate_imu_camera` while exciting all 6 axes in front of
   the grid. Expect time offset estimates in ms; residual target under 1 ms.

## 3. Pick an estimator
| Option | Type | Notes |
|---|---|---|
| OpenVINS | MSCKF filter | Light, well documented, good for embedded |
| VINS-Fusion | Sliding-window optimisation | Mono/stereo + IMU, loop closure |
| ORB-SLAM3 | Optimisation + map | Multi-map, relocalisation, best accuracy with loops |
| Basalt, Kimera | Optimisation | Fast, good on stereo |
All use IMU preintegration between keyframes (Forster et al.).

## 4. Initialisation
Monocular VIO needs motion with acceleration to observe scale and gravity: move the device in a figure-eight
for a few seconds before relying on it. Stationary starts or constant velocity leave scale unobservable.

## 5. Evaluation
```bash
evo_ape tum groundtruth.txt estimate.txt -va --align --correct_scale --plot   # ATE (mono) ; drop --correct_scale for metric VIO
evo_rpe tum groundtruth.txt estimate.txt -r trans_part --delta 1 --delta_unit m
```
Benchmarks: EuRoC MAV, TUM-VI. Report drift as a percentage of distance travelled.

## Gotchas
- Software timestamps jitter; use hardware sync or driver-level timestamps.
- Rolling-shutter cameras need RS-aware models or a global-shutter sensor.
- Wrong IMU axis convention or units (g vs m/s^2, deg vs rad) diverges immediately.
- Vibration (drones) aliases into the accelerometer: mechanical damping plus IMU low-pass filter.

## Verify
- [ ] Kalibr reprojection errors under ~0.5 px and time offset estimated; evo ATE on a loop under 1% of path
  length; return-to-start error measured.
