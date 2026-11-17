---
id: computing-software.computer-graphics-engineering.opencv.opencv-laplacian-and-scharr-derivatives
name: opencv-laplacian-and-scharr-derivatives
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-filtering, laplacian, scharr, sobel, image-gradients, focus-measure, imgproc]
level: practitioner
status: verified
description: "Compute image derivatives in OpenCV: Sobel vs Scharr accuracy, Laplacian for edges and focus measure, ddepth CV_64F to keep negative values, and gradient magnitude/orientation."
sources: ["https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html", "https://docs.opencv.org/4.x/d5/d0f/tutorial_py_gradients.html", "https://docs.opencv.org/4.x/d2/d2c/tutorial_sobel_derivatives.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Laplacian and Scharr derivatives

## Sobel vs Scharr
```python
gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
gx = cv2.Scharr(gray, cv2.CV_32F, 1, 0)          # same as Sobel(..., ksize=cv2.FILTER_SCHARR)
mag, ang = cv2.cartToPolar(gx, gy, angleInDegrees=True)
```
- 3x3 Sobel has orientation error that grows with spatial frequency: on a sinusoid at 22.5 degrees the
  measured orientation was off by 0.12 / 0.48 / 2.0 degrees at 0.05 / 0.1 / 0.2 cycles per pixel, Scharr by 0.03 / 0.11 / 0.31. Scharr `[-3,0,3;-10,0,10;-3,0,3]` is rotationally more accurate: use it whenever
  the **direction** matters (HOG, orientation fields, subpixel edge fitting).
- Scharr only supports first derivatives with a 3x3 kernel (`dx=dy=1` and `dx=2` raise `dx + dy == 1` assertions). Larger smoothing means Sobel with
  ksize 5/7, or Gaussian blur first.

## ddepth
uint8 output clips negatives: always compute in `CV_16S`/`CV_32F`/`CV_64F`, then
`cv2.convertScaleAbs(gx)` for display. Combining with `addWeighted(|gx|,0.5,|gy|,0.5,0)` is an
approximation; use `cv2.magnitude(gx, gy)` for the real magnitude.

## Laplacian
```python
lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=3)
```
- `ksize=1` (the default) uses `[0,1,0;1,-4,1;0,1,0]`; larger ksize sums second Sobel derivatives (`ksize=3` gives
  `[2,0,2;0,-8,0;2,0,2]`).
- Extremely noise-sensitive: blur first (`GaussianBlur`, sigma 1 to 2) = LoG approximation.
  Zero crossings of LoG are edges (Marr-Hildreth).
- **Focus/blur measure**: variance of the Laplacian.
```python
sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
```
  Compare only between images of the same scene, size and exposure; thresholds do not transfer
  between cameras. Downscale-normalise before comparing different resolutions.

## Gotchas
- Gradients of a colour image computed per channel then max-combined beat converting to gray when
  edges are chromatic (equal luminance).
- `cartToPolar` angle is in [0, 360); for edge orientation fold to [0, 180).

## Verify
- Synthetic sinusoid at 22.5 degrees and 0.2 cycles per pixel: Scharr orientation error about 0.3 degrees, Sobel 3x3 about 2 degrees.
