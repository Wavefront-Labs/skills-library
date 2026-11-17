---
id: computing-software.computer-graphics-engineering.computer-vision.camera-extrinsics-and-world-to-camera-transforms
name: camera-extrinsics-and-world-to-camera-transforms
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-formation, extrinsics, camera-pose, coordinate-frames, rigid-transform, camera-model]
level: practitioner
status: verified
description: "Get camera extrinsics right: world-to-camera vs camera-to-world, R|t vs camera centre, OpenCV vs OpenGL/COLMAP axis conventions, inverting poses and composing rig transforms."
sources: ["https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html", "https://szeliski.org/Book/", "https://colmap.github.io/format.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extrinsics and world-to-camera transforms

## Definitions
`x_cam = R x_world + t` (world-to-camera, "extrinsics", what OpenCV `solvePnP`, COLMAP
`images.txt` quaternion+translation store). Camera centre in world: `C = -R^T t`. Camera-to-world
pose (what most engines and NeRF `transforms.json` store): `[R^T | C]`.

Write the direction in variable names: `T_cam_world` maps world points into the camera frame;
`T_world_cam = inv(T_cam_world)`. Then `T_a_c = T_a_b @ T_b_c` composes only when inner frames match.

## Axis conventions
| System | x | y | z (forward) |
|---|---|---|---|
| OpenCV / COLMAP | right | down | +z forward |
| OpenGL / Blender camera / NeRF | right | up | -z forward |
| ROS optical frame | right | down | +z forward (body frame: x forward, z up) |
Convert OpenCV to OpenGL camera frames by flipping y and z: `T_gl = T_cv @ diag(1,-1,-1,1)` for
camera-to-world poses (right-multiply; checked: a point at (0,0,1) in the OpenCV camera frame is
(0,0,-1) in the OpenGL one and both give the same world point).

## Inverting rigid transforms
```python
def inv(T):
    R, t = T[:3, :3], T[:3, 3]
    Ti = np.eye(4); Ti[:3, :3] = R.T; Ti[:3, 3] = -R.T @ t
    return Ti
```
Matches `np.linalg.inv` (checked with `allclose`) and is cheaper; the centre `C = -R^T t` is its
translation column.

## Rig/stereo
For a stereo pair, `cv2.stereoCalibrate` returns `R, T` mapping **left camera** points into the
**right camera** frame: `x_right = R x_left + T`. Baseline = `norm(T)`.

## Gotchas
- `rvec` is axis-angle (Rodrigues), not Euler angles.
- Many datasets store camera-to-world; plugging them in as extrinsics mirrors everything behind the
  camera.
- Units: keep metres throughout; scale only at IO.

## Verify
Project a known world point (e.g. a calibration target corner) through `K [R|t]` and check it
lands on the detected pixel; check `C` matches the measured camera position.
