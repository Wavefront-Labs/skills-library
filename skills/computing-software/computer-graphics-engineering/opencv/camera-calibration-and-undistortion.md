---
id: computing-software.computer-graphics-engineering.opencv.camera-calibration-and-undistortion
name: camera-calibration-and-undistortion
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [opencv, cv2, python, camera-calibration, intrinsics, distortion-coefficients, camera-matrix, chessboard, charuco, findchessboardcorners, cornersubpix, calibratecamera, reprojection-error, undistort, initundistortrectifymap, remap, getoptimalnewcameramatrix, fisheye, solvepnp, pose-estimation, stereo-calibration, computer-vision, lens-distortion]
level: practitioner
status: verified
description: "Calibrate a camera with OpenCV: capturing good chessboard/ChArUco views, calibrateCamera, judging reprojection error, undistorting efficiently, and fisheye/solvePnP notes."
sources: ["https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html", "https://docs.opencv.org/4.x/da/d13/tutorial_aruco_calibration.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Camera calibration and undistortion with OpenCV

**Goal:** recover a camera's intrinsic matrix and lens distortion so you can undistort
images and do metric work (measurement, pose estimation, AR, stereo). Python + OpenCV 4.x.

## 1. Target and capture — where calibrations succeed or fail
- Print a chessboard (e.g. 9×6 **inner** corners, 25 mm squares) or a **ChArUco** board
  (tolerates partial views and occlusion — better for wide-angle lenses and image edges).
  Mount it **perfectly flat** (glue to glass/aluminium/foam board); a warped paper target
  corrupts everything. Measure the printed square size with calipers; printers scale.
- Fix the camera settings for the whole session and production use: resolution, focus
  (disable autofocus), zoom. Changing any of these invalidates the calibration.
- Capture **15–30 sharp images** covering the whole frame, especially corners and edges
  (that's where distortion lives), with the board tilted up to ~45° in different
  directions and at different distances. Avoid motion blur and glare.

## 2. Detect corners
```python
import cv2 as cv, numpy as np, glob
pattern = (9, 6); square = 0.025              # metres
objp = np.zeros((pattern[0]*pattern[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:pattern[0], 0:pattern[1]].T.reshape(-1, 2) * square
crit = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 1e-3)
objpts, imgpts = [], []
for f in sorted(glob.glob("calib/*.png")):
    gray = cv.cvtColor(cv.imread(f), cv.COLOR_BGR2GRAY)
    ok, corners = cv.findChessboardCorners(gray, pattern,
        cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE)
    if not ok: print("no board:", f); continue
    corners = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), crit)
    objpts.append(objp); imgpts.append(corners)
```
`cv.findChessboardCornersSB` (sector-based) exists in 4.14 and 5.0; worth trying. Corner order can come
back reversed (the same board found by the classic and SB detectors differed by 0.17 px only after
reversing one list), so compare or index corners consistently. `findChessboardCorners` already returns
refined corners on a clean image (`cornerSubPix` moved them 0.0 px in a synthetic test). Draw detections (`cv.drawChessboardCorners`) and eyeball a few.

## 3. Calibrate and judge
```python
h, w = gray.shape
rms, K, dist, rvecs, tvecs = cv.calibrateCamera(objpts, imgpts, (w, h), None, None)
print("RMS reprojection error (px):", rms); print(K); print(dist.ravel())
np.savez("camera.npz", K=K, dist=dist, size=(w, h))
```
- `K = [[fx,0,cx],[0,fy,cy],[0,0,1]]`; `dist = [k1,k2,p1,p2,k3]`.
- **RMS < ~0.5 px** is good for a decent camera; > 1 px usually means bad corners, a
  non-flat target, motion blur or a wrong square count. Compute per-image error with
  `cv.projectPoints` and drop outlier images, then recalibrate.
- Sanity: `cx, cy` near the image centre (within ~5–10% of size), `fx ≈ fy` for square
  pixels; `fx ≈ focal_mm / pixel_pitch_mm` should roughly match the datasheet.
- Low RMS with poor coverage can still extrapolate badly at the edges — coverage matters
  more than squeezing RMS.
- Strong distortion: add `cv.CALIB_RATIONAL_MODEL` (k4–k6); `dist` then has 14 entries
  (`k1,k2,p1,p2,k3,k4,k5,k6,s1..s4,tauX,tauY`, the last six stay 0 unless thin-prism/tilt flags are set;
  checked on 4.14 and 5.0). Lenses beyond ~120° FOV: use the `cv.fisheye` module
  (`cv.fisheye.calibrate`, 4 coefficients), which has its own undistortion functions.

## 4. Undistort efficiently
```python
newK, roi = cv.getOptimalNewCameraMatrix(K, dist, (w, h), alpha=0)   # 0 = crop to valid pixels, 1 = keep all (black borders)
map1, map2 = cv.initUndistortRectifyMap(K, dist, None, newK, (w, h), cv.CV_16SC2)
und = cv.remap(frame, map1, map2, cv.INTER_LINEAR)   # per frame: fast
```
Build the maps once; `cv.undistort()` per frame recomputes them and is slower for
video (4.5x slower than `remap` with prebuilt maps on a 640x480 frame, measured). If you use `newK` for undistorted images, use `newK` (and zero distortion) for any
later geometry on those images.

## 5. Using it: pose with solvePnP
```python
ok, rvec, tvec = cv.solvePnP(object_points_3d, image_points_2d, K, dist, flags=cv.SOLVEPNP_IPPE)  # planar targets
```
Pass the **original** `K, dist` with points from the distorted image (or `newK` and
`None` with points from the undistorted one) — mixing them is a common silent error.

## Gotchas
- Resolution change = rescale K (fx, fy, cx, cy scale linearly with width/height);
  distortion coefficients stay the same. Cropping changes cx, cy.
- Calibration done at one focus distance drifts if focus changes.
- Image size argument is `(width, height)`; NumPy shapes are `(height, width)`.

## Verify
- [ ] RMS reprojection error < ~0.5 px with no per-image outliers.
- [ ] Coverage includes corners/edges of the frame.
- [ ] Straight lines (door frames, the board) are straight after undistortion.
- [ ] Measuring a known distance with solvePnP agrees within a few percent.
- [ ] Calibration file stores the image size it is valid for.
