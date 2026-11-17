---
id: computing-software.computer-graphics-engineering.opencv.opencv-sepfilter2d-separable-kernels
name: opencv-sepfilter2d-separable-kernels
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-filtering, sepfilter2d, separable-filter, getgaussiankernel, getderivkernels, imgproc]
level: practitioner
status: docs-checked
description: "Use sepFilter2D for separable kernels in OpenCV: building row/column vectors, getGaussianKernel/getDerivKernels, rank-1 checks and SVD splitting."
sources: ["https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sepFilter2D: separable kernels

A 2D kernel K is separable when `K = col @ row` (rank 1). `sepFilter2D` filters every row with
`kernelX`, then every column of the result with `kernelY`, so each pixel costs two 1D passes
instead of one full 2D kernel.

```python
kx = cv2.getGaussianKernel(31, 5.0)            # 1D Gaussian, weights sum to 1
out = cv2.sepFilter2D(img, cv2.CV_32F, kx, kx)  # kernelX filters each row, kernelY each column
```

## Ready-made 1D kernels
- `cv2.getGaussianKernel(ksize, sigma, ktype=cv2.CV_64F)`; a non-positive `sigma` is computed as
  `0.3*((ksize-1)*0.5 - 1) + 0.8`. `ktype` may be `CV_32F` or `CV_64F`.
- `kx, ky = cv2.getDerivKernels(dx=1, dy=0, ksize=5, normalize=True)` gives Sobel kernels
  (`ksize=cv2.FILTER_SCHARR` gives Scharr 3x3); the docs advise normalised kernels for float
  images and `normalize=False` to keep fractional bits when an 8-bit image goes to 16-bit output.
- Box: `np.ones((k,1), np.float32)/k`.

## Splitting an arbitrary kernel
```python
U, S, Vt = np.linalg.svd(K)
if S[1] / S[0] < 1e-6:                          # effectively rank 1
    col = U[:, 0] * np.sqrt(S[0]); row = Vt[0] * np.sqrt(S[0])
```
For rank r > 1 you can sum r separable passes (low-rank approximation): worth it when r is
small and k is large.

## Gotchas
- Argument order is `(src, ddepth, kernelX, kernelY)`: `kernelX` holds the coefficients for each
  row, `kernelY` for each column. Swapping them on asymmetric kernels transposes the effect.
- `sepFilter2D` does not support `BORDER_WRAP`.
- `Sobel` uses a separable `ksize x ksize` kernel itself (except `ksize = 1`); hand-rolling
  `sepFilter2D` only helps for custom 1D kernels.
- Like `filter2D`, it computes correlation, not convolution (the kernel is not mirrored).

## Verify
`np.allclose(cv2.sepFilter2D(f, -1, kx, ky), cv2.filter2D(f, -1, ky @ kx.T), atol=1e-4)` on a
float image.

## Checked
2026-11-01. Confirmed in the OpenCV 4.x imgproc filter reference: sepFilter2D (row then column,
kernelX/kernelY roles, BORDER_WRAP), getGaussianKernel (default ktype CV_64F, sigma formula,
smoothing kernels), getDerivKernels (normalize, ktype, Scharr), Sobel separability, filter2D
correlation. Corrected: the default `ktype` (was CV_32F). Removed: the "about 15x faster"
figure, the 31x1 shape and Nx1/1xN acceptance claims, and the GaussianBlur internals claim.
The SVD rank check is plain linear algebra, not an OpenCV claim.
Method: documentation only; no commands were run.
