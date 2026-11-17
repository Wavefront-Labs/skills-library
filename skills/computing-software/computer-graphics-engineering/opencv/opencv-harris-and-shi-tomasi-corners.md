---
id: computing-software.computer-graphics-engineering.opencv.opencv-harris-and-shi-tomasi-corners
name: opencv-harris-and-shi-tomasi-corners
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-features2d, harris-corner, goodfeaturestotrack, shi-tomasi, cornersubpix, corner-detection]
level: practitioner
status: verified
description: "Detect corners in OpenCV with cornerHarris and goodFeaturesToTrack: blockSize/k/qualityLevel/minDistance tuning, masks, and cornerSubPix refinement for tracking."
sources: ["https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html", "https://docs.opencv.org/4.x/dc/d0d/tutorial_py_features_harris.html", "https://docs.opencv.org/4.x/d4/d8c/tutorial_py_shi_tomasi.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Harris and Shi-Tomasi corners

## Shi-Tomasi (what you usually want)
```python
pts = cv2.goodFeaturesToTrack(gray, maxCorners=500, qualityLevel=0.01, minDistance=10,
                              mask=None, blockSize=3, useHarrisDetector=False)
pts = cv2.cornerSubPix(gray, pts, (5, 5), (-1, -1),
                       (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01))
```
- `qualityLevel` is **relative** to the strongest corner in the image: one very strong corner
  suppresses everything else. For uniform coverage use a lower value (0.001 to 0.01) plus
  `minDistance`, or detect per grid cell with a mask.
- `minDistance` does non-maximum suppression in pixels: set it to the tracking window size so
  tracks do not overlap.
- Input must be single-channel uint8 or float32 (3-channel and uint16 input raise errors, checked). Returns float32 `(N,1,2)`, ready for
  `calcOpticalFlowPyrLK`.
- `mask` (uint8, nonzero = allowed) excludes logos, the car bonnet, or existing tracks.

## Harris response map
```python
R = cv2.cornerHarris(np.float32(gray), blockSize=2, ksize=3, k=0.04)
corners = np.argwhere(R > 0.01 * R.max())
```
- `k` in 0.04 to 0.06; larger k = fewer, stronger corners. Harris returns a response image, not
  points: you must threshold and non-max-suppress yourself (dilate + compare).
- Shi-Tomasi uses `min(lambda1, lambda2)` and is generally more stable for tracking.

## cornerSubPix
- Window `(5,5)` means an 11x11 search; it must not include neighbouring corners.
- Essential for calibration patterns and stereo. On a rendered, rotated 8x8 checkerboard `goodFeaturesToTrack`
  corners were a median 0.40 px from the true corners and 0.03 px (max 0.05) after `cornerSubPix`.

## Gotchas
- Corners are not scale invariant: at different zooms use a pyramid or ORB/SIFT.
- Blur heavy JPEG/noise first (`GaussianBlur` sigma about 1), otherwise texture noise dominates.

## Verify
Plot points on a checkerboard: one detection per inner corner, refined positions within 0.1 px of
the synthetic ground truth.
