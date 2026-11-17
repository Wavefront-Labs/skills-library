---
id: computing-software.computer-graphics-engineering.opencv.opencv-connected-components-with-stats
name: opencv-connected-components-with-stats
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, shape-analysis, connected-components, connectedcomponentswithstats, blob-analysis, labelling, distance-transform, watershed, particle-counting]
level: practitioner
status: verified
description: "Count and measure blobs with OpenCV connectedComponentsWithStats: connectivity, stats and centroids, area filtering."
sources: ["https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#ga107a78bf7cd25dec05fb4dfc5c9e765f", "https://docs.opencv.org/4.x/d3/db4/tutorial_py_watershed.html", "https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#ga8a0b7fdfcb7a13dde018988ba3a43042"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV connected components with stats

**Goal:** label every blob in a binary image and get its area, bounding box and centroid in
one fast call — the workhorse for particle counting, defect detection and mask cleanup.

## 1. Label and measure
```python
n, labels, stats, cents = cv2.connectedComponentsWithStats(mask, connectivity=8, ltype=cv2.CV_32S)
# label 0 is background
for i in range(1, n):
    x, y, w, h, area = stats[i]          # CC_STAT_LEFT, TOP, WIDTH, HEIGHT, AREA
    cx, cy = cents[i]
```
- `connectivity=8` joins diagonal neighbours, `4` doesn't — choose consistently with how
  your objects touch.
- Much faster than `findContours` + per-contour measurements when you only need
  area/box/centroid; no outline or holes info.

## 2. Remove small specks (vectorised)
```python
keep = np.zeros(n, bool); keep[1:] = stats[1:, cv2.CC_STAT_AREA] >= min_area
clean = (keep[labels] * 255).astype(np.uint8)
```
Same idea for "keep largest component": `largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])`.

## 3. Split touching objects (coins, cells, grains)
```python
dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
_, peaks = cv2.threshold(dist, 0.5 * dist.max(), 255, cv2.THRESH_BINARY)
n, markers = cv2.connectedComponents(peaks.astype(np.uint8))
sure_bg = cv2.dilate(mask, None, iterations=3)
unknown = cv2.subtract(sure_bg, peaks.astype(np.uint8))
markers = markers + 1; markers[unknown == 255] = 0
markers = cv2.watershed(cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), markers)   # boundaries = -1
count = markers.max() - 1
```
The `0.5 * max` peak threshold sets how aggressively objects split; for very different object
sizes use local maxima (`peak_local_max` from scikit-image) instead of a global ratio.

## 4. Pixel-to-real units
Areas in px² → mm² with the calibrated scale (px/mm)²; centroids through the camera model if
the lens distorts (undistort first).

## Gotchas
- Input must be single-channel 8-bit (3-channel and float32 input raise errors); any non-zero is
  foreground (a JPEG-compressed mask has noise values, 8 distinct levels in a two-square test — threshold it first).
- `ltype=CV_16U` raises "overflowed label type" once there are 65535 or more labels (a 512x512 grid of
  isolated pixels, 65536 components); use `CV_32S`.
- Watershed needs a 3-channel 8-bit image argument even when working on masks.

## Verify
- [ ] Count on a synthetic image with known number of touching circles matches.
- [ ] Area filter threshold justified from the noise blob size distribution (histogram).
- [ ] Results stable across connectivity setting for well-separated objects.
