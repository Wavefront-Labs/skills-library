---
id: computing-software.computer-graphics-engineering.opencv.opencv-projectpoints-and-drawframeaxes
name: opencv-projectpoints-and-drawframeaxes
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-calib3d, projectpoints, drawframeaxes, reprojection-error, pose-visualization, solvepnp]
level: practitioner
status: docs-checked
description: "Project 3D points to pixels with cv2.projectPoints and draw pose axes with drawFrameAxes: rvec/tvec conventions, distortion, Jacobians, and reprojection error checks."
sources: ["https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html", "https://github.com/opencv/opencv/blob/4.x/modules/calib3d/include/opencv2/calib3d.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# projectPoints and drawFrameAxes

```python
img_pts, J = cv2.projectPoints(obj_pts, rvec, tvec, K, dist)   # obj_pts (N,3) float
img_pts = img_pts.reshape(-1, 2)
```
- `rvec, tvec` perform a change of basis from the **world to the camera** coordinate system (see `calibrateCamera`), the
  pose convention `solvePnP` uses. Output points are pixel coordinates with distortion applied.
- An empty `distCoeffs` means zero distortion; use that for already-undistorted or rectified images (applying real
  coefficients to them would distort twice).
- Filter points behind the camera (non-positive camera-frame Z) yourself before projecting; the docs do not describe their handling.
- `J` is a 2N x (10 + number of distortion coefficients) Jacobian with respect to rvec, tvec, the focal lengths, the principal point and
  the distortion coefficients (for example 2N x 15 with five coefficients).

## Draw pose axes
```python
cv2.drawFrameAxes(img, K, dist, rvec, tvec, length=0.05, thickness=3)   # X red, Y green, Z blue
```
`length` is in the same unit as `tvec` (usually metres); `image` must have 1 or 3 channels; `thickness` defaults to 3.

## Reprojection error
```python
proj, _ = cv2.projectPoints(obj_pts, rvec, tvec, K, dist)
err = np.linalg.norm(proj.reshape(-1, 2) - img_pts_detected, axis=1)
print(err.mean(), err.max())
```
Check per-point error: a single large outlier means a bad correspondence, uniformly large error
means wrong intrinsics or units.

## Drawing a 3D box
Project the 8 corners of a cube and connect them with `cv2.line`; a stable box under motion is a
fast visual test of the pose pipeline.

## Gotchas
- `objectPoints` may be 3xN or Nx3 1-channel, or 1xN or Nx1 3-channel (or a vector of Point3f).
- Keep target and `tvec` in the same length unit.
- For fisheye models use `cv2.fisheye.projectPoints`.

## Verify
Project the calibration target's corners with each image's extrinsics: mean error should match
the calibration RMS.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/calib3d/include/opencv2/calib3d.hpp. Confirmed: projectPoints signature, coordinate convention, empty distCoeffs, input shapes and Jacobian size 2N x (10 + distortion coefficients) (the draft said 2N x 15), drawFrameAxes parameters and colours, fisheye.projectPoints exists. Removed the unconfirmed mirrored-point claim.
Method: documentation only; no commands were run.
