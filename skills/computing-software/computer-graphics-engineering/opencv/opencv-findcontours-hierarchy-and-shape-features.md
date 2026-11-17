---
id: computing-software.computer-graphics-engineering.opencv.opencv-findcontours-hierarchy-and-shape-features
name: opencv-findcontours-hierarchy-and-shape-features
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, contours, shape-analysis, findcontours, contour-hierarchy, image-moments, approxpolydp, convex-hull, convexity-defects, solidity, circularity, minarearect, fitellipse, matchshapes, hu-moments]
level: practitioner
status: verified
description: "Extract and measure shapes with OpenCV contours: retrieval modes and hierarchy (holes), moments and centroids, approxPolyDP, convex hull/defects, minAreaRect and shape filters."
sources: ["https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html", "https://docs.opencv.org/4.x/d9/d8b/tutorial_py_contours_hierarchy.html", "https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html", "https://docs.opencv.org/4.x/d1/d32/tutorial_py_contour_properties.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OpenCV contours: hierarchy and shape features

**Goal:** from a binary mask, get each object's outline, holes, size, position, orientation
and shape class — robustly enough for inspection and measurement.

## 1. Find contours
```python
cnts, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
```
- Input: 8-bit binary, **white objects on black** (non-zero = foreground). Invert if needed.
- Modes: `RETR_EXTERNAL` (outer only — fastest, most common), `RETR_LIST` (all, no
  relationships), `RETR_CCOMP` (2 levels: outer + holes), `RETR_TREE` (full nesting).
- `hier[0][i] = [next, prev, first_child, parent]`; with CCOMP, a contour with
  `parent != -1` is a hole of that parent.
- `CHAIN_APPROX_SIMPLE` compresses straight runs; `NONE` keeps every pixel (needed for
  curvature analysis).

## 2. Measurements
```python
for c in cnts:
    area = cv2.contourArea(c)                       # Green's formula; hole area not subtracted
    if area < 50: continue
    M = cv2.moments(c); cx, cy = M["m10"] / M["m00"], M["m01"] / M["m00"]   # centroid
    peri = cv2.arcLength(c, True)
    circularity = 4 * np.pi * area / (peri * peri)  # 1.0 = circle
    hull = cv2.convexHull(c); solidity = area / cv2.contourArea(hull)
    (rx, ry), (rw, rh), angle = cv2.minAreaRect(c)  # oriented box
    x, y, w, h = cv2.boundingRect(c)                # axis-aligned
    if len(c) >= 5: ellipse = cv2.fitEllipse(c)
```
Hu moments (`cv2.HuMoments(M)`) and `cv2.matchShapes(c1, c2, cv2.CONTOURS_MATCH_I1, 0)` give
rotation/scale-invariant shape comparison.

## 3. Polygon simplification
```python
approx = cv2.approxPolyDP(c, epsilon=0.02 * peri, closed=True)
shape = {3: "triangle", 4: "quad"}.get(len(approx), "circle" if circularity > 0.85 else "poly")
```
Epsilon relative to perimeter makes it scale-independent.

## 4. Convexity defects (fingers, notches, dents)
```python
hull_idx = cv2.convexHull(c, returnPoints=False)
defects = cv2.convexityDefects(c, hull_idx)        # rows: start, end, farthest, depth*256
deep = [d for d in defects.reshape(-1, 4) if d[3] / 256.0 > 10] if defects is not None else []
```
The result shape differs by version: `(n, 1, 4)` on 4.14 but `(n, 4)` on 5.0.0 (so the old `defects[:, 0]`
indexing breaks); `reshape(-1, 4)` works on both. Depth is `d[3] / 256.0` pixels (a 60 px notch gave 15360).

## 5. minAreaRect angle convention
The angle convention has changed between releases; on 4.14.0 and 5.0.0 a rectangle rotated through 0-180 degrees
gave angles in [-90, 0) (a 50x50 square gave -90.0). Normalise with the box's width/height
ordering before using it for rotation, or avoid the angle and use `cv2.boxPoints(rect)` corners.

## Gotchas
- Objects touching the image border get truncated contours — filter with boundingRect.
- Touching objects merge into one contour; separate with distance transform + watershed
  or erosion before contouring.
- `contourArea(c, True)` is signed (outer contours gave negative, holes positive in a ring test); the default is unsigned.
- `contourArea` of an outer contour does not subtract holes (ring: 2736 for the outer contour, hole 474 separately).
- Contours are in pixel units of the (possibly resized) mask — rescale before reporting mm.

## Verify
- [ ] Synthetic test shapes (circle, square, triangle) classified correctly at several scales.
- [ ] Hole detection works for a ring (outer + one child in hierarchy).
- [ ] Measured sizes match a calibrated reference within tolerance.
