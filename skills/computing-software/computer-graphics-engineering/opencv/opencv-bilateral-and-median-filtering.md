---
id: computing-software.computer-graphics-engineering.opencv.opencv-bilateral-and-median-filtering
name: opencv-bilateral-and-median-filtering
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-filtering, bilateral-filter, median-blur, edge-preserving, denoising]
level: practitioner
status: verified
description: "Remove noise while keeping edges with cv::medianBlur and cv::bilateralFilter: parameter choice, speed, and when to use edge-preserving filters instead."
sources: ["https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html", "https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Median and bilateral filtering

## 1. Median: impulse (salt-and-pepper) noise
```python
out = cv2.medianBlur(img, 5)        # ksize odd; > 5 only for 8-bit input
```
Removes isolated outliers completely while keeping step edges. Kernels above 5 require
8-bit images (16-bit and float32 raise an error at ksize 7, checked) and get slow; for float or large kernels downscale first.

## 2. Bilateral: Gaussian-like noise, keep edges
```python
out = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
```
- `sigmaColor`: how different in intensity a neighbour may be and still smooth (in pixel units,
  0-255 for 8-bit). Large means behaves like Gaussian blur.
- `sigmaSpace`: spatial falloff. `d` <= 0 derives the window from sigmaSpace.
- Cost grows roughly with d squared (720p colour: d=5 2 ms, d=9 14 ms, d=15 32 ms, d=25 104 ms);
  apply repeatedly with small d for a cartoon look.

## 3. Alternatives
| Need | Use |
|---|---|
| Strong smoothing, edges kept, fast | `cv2.ximgproc.guidedFilter` (contrib) or `edgePreservingFilter` (photo) |
| Best quality denoise | `fastNlMeansDenoisingColored` |
| Joint/cross filtering (depth upsampling) | `cv2.ximgproc.jointBilateralFilter` |

## Gotchas
- Bilateral filter does not work in place; `dst` must differ from `src`.
- On float images, sigmaColor is in the image's units (e.g. 0.1 for 0-1 data).
- Median on colour filters channels independently, which can create new colours at edges (a 3x3
  window of red, green and blue columns gives black).

## Verify
- [ ] Compare edge sharpness (Sobel magnitude along a known edge) before and after.
- [ ] Time the call at production resolution.
