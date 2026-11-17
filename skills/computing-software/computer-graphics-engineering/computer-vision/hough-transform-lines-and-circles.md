---
id: computing-software.computer-graphics-engineering.computer-vision.hough-transform-lines-and-circles
name: hough-transform-lines-and-circles
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, model-fitting, hough-transform, houghlines, houghlinesp, houghcircles, line-detection, lsd, accumulator, robust-estimation]
level: practitioner
status: verified
description: "Detect lines and circles with Hough transforms: accumulator resolution and thresholds, probabilistic HoughLinesP for segments, HoughCircles gradient parameters."
sources: ["https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html", "https://docs.opencv.org/4.x/d4/d70/tutorial_hough_circle.html", "https://szeliski.org/Book/", "https://docs.opencv.org/4.x/db/d73/classcv_1_1LineSegmentDetector.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hough transform for lines and circles

**Goal:** find geometric primitives (lane markings, document edges, pipes, coins, holes)
robustly despite gaps and clutter.

## 1. How it works
Each edge pixel votes for all parameter sets consistent with it; peaks in the accumulator are
detected shapes. Lines: `ρ = x cos θ + y sin θ` → (ρ, θ) space. Robust to gaps and outliers
because votes accumulate.

## 2. Lines
```python
edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 180, threshold=150)       # infinite lines (ρ, θ)
segs  = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=50,
                        minLineLength=40, maxLineGap=10)                      # segments x1,y1,x2,y2
```
- `threshold` = minimum votes ≈ minimum number of edge pixels on the line — scale with image size
  (tested: a 150-pixel line was found with threshold 149 and not with 150, so a line needs strictly
  more votes than `threshold`).
- `rho`/`theta` resolution trade precision vs vote splitting; 1 px / 1° is standard.
- Restrict θ range (`min_theta/max_theta`) when you know orientation (near-vertical lines).
- Post-process: merge near-duplicate lines (cluster by ρ, θ), refine each with least squares on
  its inlier edge points.

## 3. Circles (gradient method)
```python
circles = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                           param1=120, param2=40, minRadius=10, maxRadius=80)
# HOUGH_GRADIENT_ALT: param2 is a 0-1 circularity score (~0.9), more accurate; docs recommend
# dp=1.5 and a higher param1 (about 300) because it uses Scharr derivatives
```
- `param1`: upper Canny threshold (computed internally); `param2`: accumulator threshold —
  lower finds more (and false) circles.
- **Always bound radii** — unbounded search is slow and noisy.
- `minDist` between centres prevents duplicates of the same circle.

## 4. Alternatives
- **LSD / `cv2.createLineSegmentDetector`** (works in OpenCV 5.0.0) or `ximgproc.FastLineDetector`:
  sub-pixel segments, no parameter tuning per image — often better than HoughLinesP.
- **RANSAC** line/circle fitting when you have a ROI with one dominant shape: more accurate
  parameters.
- `cv2.fitEllipse` on contours for ellipses (Hough for ellipses is expensive).

## Gotchas
- Results depend heavily on edge map quality; tune Canny first.
- Textured backgrounds generate many spurious peaks — mask the ROI.
- Hough line angles: θ ∈ [0, π); vertical lines have θ ≈ 0, horizontal ≈ π/2.

## Verify
- [ ] Precision/recall on labelled images across lighting conditions.
- [ ] Detected parameters refined and compared against ground-truth geometry (px error).
- [ ] Runtime within budget (radius bounds and ROI applied).
