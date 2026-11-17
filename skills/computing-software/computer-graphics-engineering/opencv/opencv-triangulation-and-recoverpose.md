---
id: computing-software.computer-graphics-engineering.opencv.opencv-triangulation-and-recoverpose
name: opencv-triangulation-and-recoverpose
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-calib3d, triangulatepoints, recoverpose, essential-matrix, two-view-geometry]
level: advanced
status: docs-checked
description: "Recover relative camera pose from an essential matrix with cv::recoverPose and triangulate 3D points with triangulatePoints, handling scale and cheirality."
sources: ["https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html", "https://docs.opencv.org/4.x/d0/dbd/group__triangulation.html", "https://github.com/opencv/opencv/blob/4.x/modules/calib3d/include/opencv2/calib3d.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Two-view pose and triangulation

## 1. Essential matrix and pose
```python
E, inl = cv2.findEssentialMat(p1, p2, K, method=cv2.USAC_MAGSAC, prob=0.999, threshold=1.0)
n, R, t, inl = cv2.recoverPose(E, p1, p2, K, mask=inl)
```
- `recoverPose` decomposes E with `decomposeEssentialMat` and verifies the pose hypotheses with a chirality check (triangulated points must
  have positive depth). The returned integer counts inliers that pass; in the output mask only inliers that pass the chirality check remain.
- `t` is known only up to scale: it is the direction of the translation and has unit length.
- This overload assumes both images come from cameras with the same intrinsic matrix. For two cameras, use the overload taking
  `cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2` (with `findEssentialMat`'s two-camera overload), or the `focal` and `pp` overload for a shared focal length.

## 2. Triangulate
```python
P1 = K @ np.hstack([np.eye(3), np.zeros((3, 1))])
P2 = K @ np.hstack([R, t])
X = cv2.triangulatePoints(P1, P2, p1[inl.ravel() > 0].T, p2[inl.ravel() > 0].T)  # 4xN homogeneous
X = (X[:3] / X[3]).T
```
Per the docs, `projPoints` are 2xN arrays and all input data must be of float type. The 4xN result is homogeneous and is
returned in the coordinate system the projection matrices are defined in (here camera 1).

## 3. Filter
- Reprojection error per point in both views; drop points above a threshold you choose for your sensor.
- Parallax angle between rays; drop points with very small parallax, where depth is unreliable.
- Positive depth in both cameras.

## Gotchas
- `findEssentialMat` needs at least 5 points; the camera matrix passed in must match the points' camera.
- Undistort the points, or pass the distortion coefficients through the overloads that accept them.

## Verify
- [ ] Reprojection error is small for your setup; a synthetic test with known R, t recovers them (t up to scale).

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/calib3d/include/opencv2/calib3d.hpp. Confirmed: recoverPose overloads, chirality check, unit-length t, mask semantics, triangulatePoints input and output conventions and float requirement, findEssentialMat parameters. Removed the unconfirmed numeric thresholds and the degeneracy and DLT statements.
Method: documentation only; no commands were run.
