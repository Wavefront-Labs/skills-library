---
id: computing-software.robotics-software.robot-perception-slam.camera-calibration
name: camera-calibration
category: computing-software
field: robotics-software
product: robot-perception-slam
tags: [camera-calibration, checkerboard, camera-info, intrinsics, ost-yaml, distortion, perception-camera]
level: practitioner
status: docs-checked
description: "Calibrate a monocular or stereo camera with camera_calibration and publish CameraInfo."
sources:
  - https://github.com/ros-perception/image_pipeline/blob/rolling/camera_calibration/doc/tutorial_mono.rst
  - https://github.com/ros-perception/image_pipeline/blob/rolling/camera_calibration/doc/tutorial_stereo.rst
  - https://github.com/ros-perception/image_pipeline/blob/rolling/camera_calibration/doc/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Camera calibration
```bash
ros2 run camera_calibration cameracalibrator --size 8x6 --square 0.108 image:=/camera/image_raw camera:=/camera
```
- `--size` counts interior corners of the chessboard (columns x rows), not squares; `--square` is the square side in metres. To use several boards, give several `--size`/`--square` pairs. If the window does not open, `--no-service-check` is the documented workaround.
- Move the board to the left, right, top and bottom of the field of view, fill the view, and tilt it. Three bars in the sidebar (X, Y, size/skew) grow; when the **CALIBRATE** button lights, you have enough data. Calibration can take about a minute.
- Results: camera matrix (K), distortion, rectification and projection matrices. The distortion model for pinhole cameras is `plumb_bob`. **COMMIT** sends the parameters to the camera for permanent storage; the camera driver can also load a YAML file with its `camera_info_url` parameter.
- Stereo: `ros2 run camera_calibration cameracalibrator --approximate 0.1 --size 8x6 --square 0.108 right:=/stereo/right/image_raw left:=/stereo/left/image_raw left_camera:=/stereo/left right_camera:=/stereo/right`.
- Loading a calibration file does not rectify the image; use the `image_proc` package for that.

## Gotchas
- If no coloured dots appear, count interior vertex points, not squares.
- Calibrate at the resolution and focus you will run; changes invalidate it.

## Self-check
Rectified straight lines (door frames) look straight in the `image_rect` output.

## Checked
2026-11-03. Confirmed in the camera_calibration mono and stereo tutorials and index page of ros-perception/image_pipeline (command forms, `--size`, `--square`, `--approximate`, `--no-service-check`, sidebar bars, CALIBRATE and COMMIT, `plumb_bob`, `camera_info_url`, rectification via image_proc). Removed: the `--ros-args -r` remap form (the tool takes plain `image:=`/`camera:=` arguments), the apt install line, the SAVE button step, the 0.5 pixel error target and the `camera_info_manager` pairing.
Method: documentation only; no commands were run.
