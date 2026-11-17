---
id: computing-software.computer-graphics-engineering.computer-vision.rolling-shutter-handling
name: rolling-shutter-handling
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-formation, camera-model, rolling-shutter, global-shutter, line-delay, readout-time, imu-camera-sync, hardware-trigger]
level: advanced
status: draft
description: "Recognise and handle rolling-shutter distortion in vision systems: measure readout time, choose global-shutter sensors, sync IMU/camera timestamps."
sources: ["https://szeliski.org/Book/", "https://arxiv.org/abs/1807.01452", "https://github.com/ethz-asl/kalibr/wiki/Rolling-Shutter-Camera-calibration", "https://docs.opencv.org/4.x/d4/d94/tutorial_camera_calibration.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rolling shutter handling

**Goal:** accurate geometry from moving cameras or moving objects despite CMOS sensors
that expose rows at different times (Szeliski 2e §2.3).

## 1. Know the effect
Each row is exposed `readout / H` seconds after the previous one. With readout 10–30 ms
(typical phone/webcam) and fast motion:
- Skew of vertical lines under horizontal pan; wobble ("jello") under vibration.
- Fast objects (propellers, balls) distorted.
- SLAM/VO pose errors and calibration bias if frames are treated as instantaneous.

## 2. Measure the readout time
- Datasheet: frame readout / line time (`t_line`) at the used resolution and mode.
- Empirical: film a flashing LED at known frequency or a fast-spinning disk; count the band
  pattern across rows. Or pan past a vertical edge at known angular rate and measure skew.
- Kalibr can estimate line delay during camera calibration (rolling-shutter model).

## 3. Avoid it (best option)
- **Global-shutter** sensors for robotics, metrology, high-speed inspection (e.g. Sony Pregius,
  OV9281). Lower resolution/sensitivity, but no row timing.
- Short exposure doesn't remove rolling shutter (readout still sequential) — it reduces blur only.
- Reduce readout time: lower resolution/cropped modes, higher pixel clock.

## 4. Model it
- Timestamp per row: `t_row = t_frame_start + row * t_line` (check whether the driver
  timestamp is start, middle, or end of exposure/readout!).
- VIO/SLAM: rolling-shutter-aware projection (pose interpolated per row from IMU or
  continuous-time splines, as in Basalt/OpenVINS/Kalibr) — required for accurate phone VIO.
- Calibration: keep the target still (or the camera on a tripod) during capture, so rolling
  shutter doesn't bias intrinsics.
- Stabilisation: per-row warps (mesh-based) instead of single homographies.

## 5. Synchronisation
Hardware trigger + strobe output to align camera exposures with other cameras, IMU, lidar;
software timestamps can be off by tens of ms. Estimate residual time offset camera↔IMU
(Kalibr `--time-calibration`, OpenVINS online calibration).

## Gotchas
- Multi-camera stereo with rolling shutters: rows must be synchronised and same orientation,
  or depth is wrong for moving scenes.
- Event-based and line-scan cameras have their own timing models — don't reuse frame models.

## Verify
- [ ] Readout time measured and recorded with the camera mode settings.
- [ ] Fast-pan test: reconstruction/pose error compared with and without the rolling-shutter model.
- [ ] Camera-IMU time offset estimated (< 1 ms residual) where VIO is used.
