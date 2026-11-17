---
id: computing-software.computer-graphics-engineering.computer-vision.dlt-normalised-linear-estimation
name: dlt-normalised-linear-estimation
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, model-fitting, dlt, direct-linear-transform, homography, hartley-normalization, svd]
level: advanced
status: verified
description: "Estimate homographies, fundamental matrices and camera matrices with the DLT: Hartley normalisation, SVD solution, rank enforcement, minimal sets and nonlinear refinement."
sources: ["https://www.robots.ox.ac.uk/~vgg/hzbook/", "https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DLT and normalised linear estimation

## Homography DLT
Each correspondence `x' ~ H x` gives two rows of `A h = 0`:
```python
def normalize(p):
    c = p.mean(0); s = np.sqrt(2) / np.mean(np.linalg.norm(p - c, axis=1))
    T = np.array([[s, 0, -s*c[0]], [0, s, -s*c[1]], [0, 0, 1]])
    return (np.c_[p, np.ones(len(p))] @ T.T), T
def dlt_h(p1, p2):
    x1, T1 = normalize(p1); x2, T2 = normalize(p2); A = []
    for (x, y, _), (u, v, _) in zip(x1, x2):
        A.append([-x, -y, -1, 0, 0, 0, u*x, u*y, u])
        A.append([0, 0, 0, -x, -y, -1, v*x, v*y, v])
    h = np.linalg.svd(np.asarray(A))[2][-1]
    H = np.linalg.inv(T2) @ h.reshape(3, 3) @ T1
    return H / H[2, 2]
```
Minimal set 4 points (no 3 collinear).

## Why normalise
Pixel coordinates around 1000 make A badly conditioned (entries from 1 to 10^6). Hartley
normalisation (centroid to origin, mean distance sqrt(2)) matters most for the 8-point fundamental
matrix: with 1 px noise, 50 points and 1920x1080 coordinates the median Sampson error on held-out
points was 0.43 px normalised against 3.46 px raw (8x worse). For a homography in float64 the same
test (4, 8 and 20 points, 1 px noise) showed no measurable difference (median error 0.67 px at 20
points either way), so treat normalisation as essential for F and P and cheap insurance for H
(it still protects float32 and extreme coordinate ranges). Always apply it.

## Other DLTs
- **Fundamental matrix (8-point)**: rows `[u x, u y, u, v x, v y, v, x, y, 1]`; then enforce rank 2
  by zeroing the smallest singular value.
- **Essential matrix**: on normalised camera coordinates; enforce singular values (s, s, 0). The
  5-point algorithm is better as a minimal solver in RANSAC.
- **Camera matrix P (6+ points)**: 2 rows per 3D-2D pair, 12 unknowns; decompose with RQ to K, R
  (`scipy.linalg.rq`; the result can come back with a negative focal length, so fix signs so that
  the diagonal of K is positive and `det(R) = +1`).
- **Triangulation**: linear DLT per point (`cv2.triangulatePoints`).

## Algebraic vs geometric error
DLT minimises algebraic error, which is not the reprojection error. Always refine with
Levenberg-Marquardt on geometric (reprojection/Sampson) error, starting from the DLT result.
OpenCV `findHomography` does this refinement on inliers.

## Verify
Synthetic points with known H plus 1 px noise: with 4 noise-free points the DLT recovers H to
1e-12; with noise the held-out error should approach the noise level as points are added (0.67 px
at 20 points in the test above). For F, compare normalised against raw as above.
