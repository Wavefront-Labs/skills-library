---
id: computing-software.computer-graphics-engineering.computer-vision.line-and-plane-fitting-total-least-squares
name: line-and-plane-fitting-total-least-squares
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, model-fitting, line-fitting, plane-fitting, total-least-squares, fitline, ransac]
level: practitioner
status: verified
description: "Fit lines and planes to points: total least squares via SVD/PCA, cv2.fitLine with robust distances, RANSAC for outliers, and residual/uncertainty checks."
sources: ["https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html", "https://www.open3d.org/docs/release/tutorial/geometry/pointcloud.html", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Line and plane fitting (total least squares)

## Why not y = ax + b
Ordinary least squares minimises vertical error and fails for steep lines. Total least squares
minimises perpendicular distance: the best line/plane passes through the centroid along the
principal directions.

## Plane via SVD
```python
def fit_plane(P):                  # P: (N,3)
    c = P.mean(0)
    _, s, Vt = np.linalg.svd(P - c, full_matrices=False)
    n = Vt[2]                      # normal = direction of least variance
    d = -n @ c                     # plane: n.x + d = 0
    rms = s[2] / np.sqrt(len(P))   # RMS orthogonal residual
    return n, d, rms
```
Line in 2D/3D: direction is `Vt[0]`. Ratio `s[1]/s[0]` (2D) or `s[2]/s[1]` (3D) tells how
line-/plane-like the data is.

## OpenCV fitLine (robust M-estimators)
```python
vx, vy, x0, y0 = cv2.fitLine(pts, cv2.DIST_HUBER, 0, 0.01, 0.01).ravel()
```
`DIST_L2` is plain TLS; `DIST_HUBER`, `DIST_FAIR`, `DIST_WELSCH` iteratively reweight to resist
moderate outliers. Works for 3D points too (returns 6 values). Tested on a line of true direction
(0.894, 0.447) with every tenth point shifted by 40: L2 gave (0.885, 0.465), Huber and Fair gave
(0.895, 0.446), Welsch (0.895, 0.446).

## Gross outliers: RANSAC first
```python
plane, inliers = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)  # Open3D
```
Then refit TLS on the inliers. Threshold about 2 to 3 times the sensor noise sigma.

## Multiple lines/planes
Sequential RANSAC (fit, remove inliers, repeat) or Hough for lines in images. For edge pixels in
images prefer `cv2.HoughLinesP` or LSD (`cv2.createLineSegmentDetector`) then refine each segment
with fitLine.

## Uncertainty
Normal covariance is roughly `sigma^2 / (N * lambda_i)` along each in-plane direction, with
`lambda_i` the variance of the points along that direction: points spread over a larger area give a
better-determined normal. Checked by simulation (300 points uniform on a 2 x 2 plane, sigma 0.01):
tilt error 0.0014 rad rms against a prediction of `sqrt(2) * sigma / sqrt(N * 1/3)` = 0.0014 (two
in-plane directions).

## Verify
Synthetic noisy plane with known normal: angle error well under 1 degree for a few hundred points
with 1 percent noise (measured 0.02 to 0.08 degrees for 100 to 1000 points with noise along the
normal, 0.19 degrees at 300 points with 1 percent isotropic noise); `s[2] / sqrt(N)` matched the
directly computed RMS residual to 1e-14; check residual histogram is symmetric.
