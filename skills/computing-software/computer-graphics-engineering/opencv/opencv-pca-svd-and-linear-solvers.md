---
id: computing-software.computer-graphics-engineering.opencv.opencv-pca-svd-and-linear-solvers
name: opencv-pca-svd-and-linear-solvers
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-core, cv-pca, cv-svd, cv-solve]
level: advanced
status: docs-checked
description: "Use OpenCV's linear algebra: cv::PCA for orientation and compression, SVD::compute, cv::solve with DECOMP_SVD/QR for least squares, and eigen decomposition."
sources: ["https://docs.opencv.org/4.x/d3/d8d/classcv_1_1PCA.html", "https://docs.opencv.org/4.x/df/df7/classcv_1_1SVD.html", "https://docs.opencv.org/4.x/d1/dee/tutorial_introduction_to_pca.html", "https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga12b43690dbd31fed96f213eefead2373"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PCA, SVD and linear solvers

## PCA: object orientation from contour points
```python
pts = contour.reshape(-1, 2).astype(np.float64)
mean, eigvecs, eigvals = cv2.PCACompute2(pts, mean=None)
angle = np.degrees(np.arctan2(eigvecs[0, 1], eigvecs[0, 0]))   # main axis
elongation = np.sqrt(eigvals[0, 0] / eigvals[1, 0])
```
C++: `cv::PCA pca(data, cv::Mat(), cv::PCA::DATA_AS_ROW, maxComponents);` then
`pca.project(x)` / `pca.backProject(y)` for compression and reconstruction (e.g. eigenfaces,
descriptor dimensionality reduction). The `retainedVariance` overload lets PCA decide how many components to keep for a given
variance percentage.

## SVD
```cpp
cv::Mat w, u, vt;
cv::SVD::compute(A, w, u, vt, cv::SVD::FULL_UV);       // A = u * diag(w) * vt
```
Conditioning: `invert` with `DECOMP_SVD` returns the inverse condition number (smallest over largest singular value); a tiny value means ill-conditioned (normalise inputs for DLT).

## Solving linear systems
```cpp
cv::solve(A, b, x, cv::DECOMP_LU);           // square, well-conditioned
cv::solve(A, b, x, cv::DECOMP_SVD);          // least squares, rank-deficient safe
cv::solve(A, b, x, cv::DECOMP_QR | cv::DECOMP_NORMAL);   // DECOMP_NORMAL combines with the other methods
cv::eigen(symmetricM, evals, evecs);         // symmetric only; eigenNonSymmetric otherwise
cv::invert(M, Minv, cv::DECOMP_SVD);          // pseudo-inverse
```

## When to use Eigen/NumPy instead
For NumPy code, `np.linalg.lstsq` and `np.linalg.svd` are equivalent alternatives. For large sparse systems use a sparse solver library rather than these dense routines.

## Gotchas
- Prefer float64 for geometry.
- `PCACompute2` expects rows as samples; transposed input gives nonsense axes.
- Eigenvector sign is arbitrary; normalise sign before comparing orientations across frames.

## Verify
- [ ] Synthetic tests: PCA angle of a rotated ellipse within 0.5 degrees; least-squares plane residuals match NumPy.

## Checked
Checked 2026-10-28 against OpenCV 4.13.0 docs: cv::PCA, cv::SVD, core array functions (solve, invert, eigen, PCACompute2, PCABackProject), introduction-to-PCA tutorial.
- Confirmed: `PCACompute2` Python signature returning mean, eigenvectors, eigenvalues, `PCA::DATA_AS_ROW`, `project`/`backProject`, `retainedVariance` overload, `SVD::FULL_UV`, `DecompTypes` (LU, SVD, EIG, CHOLESKY, QR, NORMAL combinable), `eigenNonSymmetric`, `invert` pseudo-inverse and inverse condition number with DECOMP_SVD.
- Removed: "faster than SVD" claim, 0.95 example, float32 precision claim and the Eigen/Ceres suggestions as facts.
- Also removed: the nullspace-from-vt recipe and the plane-fit example (not documented on the fetched pages).

Method: documentation only; no commands were run.
