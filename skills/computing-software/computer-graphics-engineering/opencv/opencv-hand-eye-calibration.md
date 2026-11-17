---
id: computing-software.computer-graphics-engineering.opencv.opencv-hand-eye-calibration
name: opencv-hand-eye-calibration
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-calib3d, hand-eye-calibration, calibratehandeye, robot-camera-calibration, eye-in-hand]
level: advanced
status: docs-checked
description: "Solve robot hand-eye calibration (eye-in-hand and eye-to-hand) with cv::calibrateHandEye and calibrateRobotWorldHandEye from pose pairs."
sources: ["https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html", "https://github.com/opencv/opencv/blob/4.x/modules/calib3d/include/opencv2/calib3d.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hand-eye calibration

**Goal:** find the fixed transform between a robot flange (gripper) and a camera.

## 1. Collect pose pairs
For each robot pose with a calibration board in view:
- `R_gripper2base, t_gripper2base` from robot forward kinematics.
- `R_target2cam, t_target2cam` from a PnP pose estimate of the board (for example `solvePnP`).
The docs require a minimum of 2 motions with non-parallel rotation axes, so at least 3 different poses, and strongly recommend
many more.

## 2. Solve (eye-in-hand)
```python
R_cam2gripper, t_cam2gripper = cv2.calibrateHandEye(
    R_gripper2base, t_gripper2base, R_target2cam, t_target2cam,
    method=cv2.CALIB_HAND_EYE_PARK)       # TSAI (default), PARK, HORAUD, ANDREFF, DANIILIDIS
```
Eye-to-hand (a static camera observing a pattern mounted on the end-effector): the docs say to input the suitable transformations,
which in the equations means supplying the base-to-gripper transform in the gripper-to-base arguments; the result is then the camera-to-base transform.

## 3. Robot-world variant
`cv2.calibrateRobotWorldHandEye` takes world-to-camera and base-to-gripper poses and returns base-to-world and gripper-to-camera
transforms (AX = ZB form); at least 3 measurements are required. Methods: `CALIB_ROBOT_WORLD_HAND_EYE_SHAH` (default) and `..._LI`.

## 4. Validate
Chain the transforms for each pose to predict the board pose in the base frame; with a correct result these predictions agree.
Report the spread in length units and degrees.

## Gotchas
- Translation units must match between the robot poses and the PnP poses; the board square size sets the PnP units.
- Convert robot controller Euler angles to rotation matrices using the controller's documented convention.
- Compare the five methods: large disagreement suggests poor input data.

## Verify
- [ ] Predicted board pose spread across poses is within your accuracy requirement.
- [ ] Touch-test: command the tool tip to a detected point; error within tolerance.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/calib3d/include/opencv2/calib3d.hpp. Confirmed: calibrateHandEye and calibrateRobotWorldHandEye signatures, method constants and defaults, eye-in-hand and eye-to-hand description, minimum pose counts. Removed the unconfirmed 10-20 pose count, 30 degree rule, ChArUco and scipy statements.
Method: documentation only; no commands were run.
