---
id: computing-software.computer-graphics-engineering.opencv.opencv-calchist-and-back-projection
name: opencv-calchist-and-back-projection
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-color-threshold, calchist, back-projection, histograms, comparehist]
level: practitioner
status: verified
description: "Compute 1D/2D histograms with cv::calcHist, compare them, and back-project a hue-saturation model to segment or track coloured objects."
sources: ["https://docs.opencv.org/4.x/d8/dbc/tutorial_histogram_calculation.html", "https://docs.opencv.org/4.x/da/d7f/tutorial_back_projection.html", "https://docs.opencv.org/4.x/d8/dc8/tutorial_histogram_comparison.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Histograms and back projection

## 1. calcHist
```python
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (0, 60, 32), (180, 255, 255))      # drop dark / unsaturated pixels
hist = cv2.calcHist([hsv], [0, 1], mask, [30, 32], [0, 180, 0, 256])  # H-S 2D histogram
cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
```
- Hue range for 8-bit is **0-180**, not 0-360. Ranges are upper-exclusive.
- `channels`, `histSize`, `ranges` are lists, one entry per dimension.

## 2. Back projection
```python
prob = cv2.calcBackProject([hsv_frame], [0, 1], hist, [0, 180, 0, 256], scale=1)
prob = cv2.filter2D(prob, -1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
_, m = cv2.threshold(prob, 50, 255, cv2.THRESH_BINARY)
```
Each pixel gets the histogram value of its colour: a likelihood map for the model colour. Feed
it to `meanShift`/`CamShift` for tracking or threshold it for segmentation.

## 3. Comparing histograms
`cv2.compareHist(h1, h2, method)`: `HISTCMP_CORREL` (1 = identical), `HISTCMP_CHISQR`
(0 = identical), `HISTCMP_INTERSECT`, `HISTCMP_BHATTACHARYYA` (0 = identical). Normalise both
first. Hue-saturation histograms are fairly robust to lighting; grey histograms are not.

## Gotchas
- Hue is undefined for greys; the saturation/value mask matters more than bin count.
- Too many bins makes the model brittle; 16-32 per axis is typical.
- `calcHist` returns float32 and `calcBackProject` returns uint8 (0-255 after the normalise above);
  normalise to 0-255 for a viewable map.

## Verify
- [ ] Back-projection of the ROI itself is bright inside, dark elsewhere.
