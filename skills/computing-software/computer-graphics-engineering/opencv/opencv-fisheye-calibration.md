---
id: computing-software.computer-graphics-engineering.opencv.opencv-fisheye-calibration
name: opencv-fisheye-calibration
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-calib3d, fisheye-calibration, kannala-brandt, undistortion, wide-angle, camera-calibration]
level: advanced
status: verified
description: "Calibrate fisheye lenses with cv2.fisheye: Kannala-Brandt model, calibrate flags, input array shapes, balance/new K for undistortion, and when to use omnidir instead."
sources: ["https://docs.opencv.org/4.x/db/d58/group__calib3d__fisheye.html", "https://docs.opencv.org/4.x/dd/d12/tutorial_omnidir_calib_main.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fisheye calibration with cv2.fisheye

The standard `calibrateCamera` (Brown-Conrady) model is commonly said to fail beyond about 120 degrees FOV (rule of thumb, not tested here). The
`cv2.fisheye` module uses the equidistant Kannala-Brandt model:
`theta_d = theta (1 + k1 theta^2 + k2 theta^4 + k3 theta^6 + k4 theta^8)`.

## Calibrate
```python
objp = np.zeros((1, nx * ny, 3), np.float64)
objp[0, :, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2) * square
# imgpoints: list of (1, N, 2) float64 arrays from findChessboardCorners + cornerSubPix
K = np.zeros((3, 3)); D = np.zeros((4, 1))
# OpenCV 4.x: cv2.fisheye.CALIB_*; OpenCV 5.0 moved them to cv2.CALIB_* (cv2.fisheye.CALIB_FIX_SKEW raises AttributeError there)
F = cv2.fisheye if hasattr(cv2.fisheye, "CALIB_FIX_SKEW") else cv2
flags = F.CALIB_RECOMPUTE_EXTRINSIC | F.CALIB_CHECK_COND | F.CALIB_FIX_SKEW
rms, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
    objpoints, imgpoints, gray.shape[::-1], K, D, flags=flags,
    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-6))
```
- Shapes matter: object points `(1,N,3)` and image points `(1,N,2)`, float64 (float32 was also accepted). `(N,3)` arrays give a
  cryptic assertion failure (`objectPoints.type() == CV_32FC3 || CV_64FC3`). Hard-coded integer flag values from 4.x do
  not carry over to 5.0 (they gave RMS 4.2 instead of 1e-7 on synthetic data); use the named constants.
- `CALIB_CHECK_COND` throws on ill-conditioned views; remove the offending image (usually a board
  too close or too oblique) rather than dropping the flag.
- Cover the **edges** of the image: fisheye distortion is largest there and boards in the centre
  only cannot constrain k3/k4.

## Undistort
```python
newK = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, (w, h), np.eye(3), balance=0.5)
m1, m2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), newK, (w, h), cv2.CV_16SC2)
und = cv2.remap(img, m1, m2, cv2.INTER_LINEAR)
```
`balance=0` crops to valid pixels, `1` keeps the full FOV with stretched borders (new focal length 243 vs 196 px on a
640x480 synthetic lens, 4.14.0). Perspective
undistortion of a 180+ degree lens cannot keep the full FOV: reproject to cylindrical/equirect
instead.

## Points
`cv2.fisheye.undistortPoints(pts, K, D, P=newK)`; `cv2.fisheye.projectPoints` for reprojection.

## Over 180 degrees / catadioptric
Use `cv2.omnidir` (Mei unified model, contrib) or Scaramuzza's OCamCalib.

## Verify
RMS under about 0.5 px; straight lines in the scene straight after undistortion across the whole
frame, especially near the edges.
