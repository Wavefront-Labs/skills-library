---
id: computing-software.computer-graphics-engineering.opencv.opencv-image-pyramids
name: opencv-image-pyramids
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-filtering, image-pyramids, pyrdown, pyrup, laplacian-pyramid]
level: practitioner
status: docs-checked
description: "Build Gaussian and Laplacian pyramids with cv::pyrDown/pyrUp for coarse-to-fine search, blending and multi-scale detection."
sources: ["https://docs.opencv.org/4.x/d4/d1f/tutorial_pyramids.html", "https://docs.opencv.org/4.x/dc/dff/tutorial_py_pyramids.html", "https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image pyramids

## 1. Gaussian pyramid
```python
levels = [img]
for _ in range(4):
    levels.append(cv2.pyrDown(levels[-1]))     # blur with the 5x5 pyramid kernel, then drop rows/cols
```
By default each level is `((w+1)//2, (h+1)//2)`. Use it for coarse-to-fine template matching and
fast multi-scale detection.

## 2. Laplacian pyramid
A level is the Gaussian level minus the upsampled next level (OpenCV has no dedicated function).
```python
lap = []
for i in range(len(levels) - 1):
    up = cv2.pyrUp(levels[i + 1], dstsize=levels[i].shape[1::-1])
    lap.append(cv2.subtract(levels[i].astype(np.float32), up.astype(np.float32)))
lap.append(levels[-1].astype(np.float32))
```
Reconstruct by `pyrUp` and add from the top. Pass `dstsize` to `pyrUp` so odd sizes match: the
docs require `|dstsize.width - 2*src.cols| <= dstsize.width mod 2` (same for height).
Store band-pass levels as float (they are signed).

## 3. Laplacian blending (seamless mask blend)
The Python pyramid tutorial blends two images by building Laplacian pyramids of both, joining the
halves at each level, then collapsing. A Gaussian pyramid of a mask gives a soft per-level
transition.

## Gotchas
- `pyrDown` blurs before it downsamples, so it is not a bare decimation.
- 8-bit subtraction clips negatives; use float for Laplacian levels.
- Coordinates scale by 2 per level: map detections back with `x * 2**level`.
- `pyrDown` requires `|dstsize.width*2 - src.cols| <= 2` (same for height) when you pass `dstsize`.

## Verify
- [ ] Reconstructing a Laplacian pyramid gives max abs error below 1 grey level.

## Checked
2026-11-01. Confirmed against the OpenCV 4.x imgproc filter reference (pyrDown, pyrUp: default
output size, 5x5 kernel, dstsize conditions, upsample-then-blur) and the C++/Python pyramid tutorials
(Laplacian level definition, blending procedure). Removed: the optical-flow `maxLevel` remark, the
claim that this is the stitching multiband blender, and the `resize` INTER_AREA comparison.
Method: documentation only; no commands were run.
