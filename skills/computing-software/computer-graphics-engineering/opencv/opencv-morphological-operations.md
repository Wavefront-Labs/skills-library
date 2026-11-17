---
id: computing-software.computer-graphics-engineering.opencv.opencv-morphological-operations
name: opencv-morphological-operations
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, image-filtering, morphological-operations, morphologyex, erode, dilate, opening, closing, top-hat, black-hat, morphological-gradient, structuring-element]
level: practitioner
status: verified
description: "Clean and analyse binary and grayscale images with OpenCV morphology: erode/dilate, opening/closing, gradient, top-hat/black-hat, structuring element shape and size choices."
sources: ["https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html", "https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga67493776e3ad1a3df63883829375201f", "https://docs.opencv.org/4.x/dd/dd7/tutorial_morph_lines_detection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV morphological operations

**Goal:** remove noise, fill gaps, separate or join shapes, and extract thin structures
from masks and grayscale images with predictable results.

## 1. Structuring element
```python
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))   # RECT, ELLIPSE, CROSS
```
- Size ≈ the feature size you want to remove/fill (e.g. specks up to 4 px → 5x5; a 4x4 speck was removed by a 5x5 ellipse opening).
- ELLIPSE avoids blocky, direction-biased results of RECT on curved objects.
- Line elements extract oriented structures: `(1, 40)` vertical, `(40, 1)` horizontal
  (table-line detection in documents).

## 2. Operations
| op | call | effect |
|---|---|---|
| erode | `cv2.erode(m, k)` | shrink white, remove specks smaller than k |
| dilate | `cv2.dilate(m, k)` | grow white, bridge gaps |
| opening | `morphologyEx(m, MORPH_OPEN, k)` | erode→dilate: remove small white noise, keep size |
| closing | `morphologyEx(m, MORPH_CLOSE, k)` | dilate→erode: fill small holes/gaps |
| gradient | `MORPH_GRADIENT` | dilate − erode: outlines |
| top-hat | `MORPH_TOPHAT` | image − opening: small bright details on uneven background |
| black-hat | `MORPH_BLACKHAT` | closing − image: small dark details (text, scratches) |
| hit-or-miss | `MORPH_HITMISS` | exact binary pattern matching (kernel: 1 = must be foreground, -1 = must be background, 0 = ignore; an int8 kernel with -1 worked, an isolated pixel matched `[-1,-1,-1;-1,1,-1;-1,-1,-1]` and stopped matching with a neighbour) |
`iterations=n` repeats; 3 iterations of a 3x3 `np.ones` (RECT) kernel equal one 7x7 RECT kernel exactly (checked). A 3x3
`MORPH_ELLIPSE` is a plus-shaped cross, so 3 iterations give a diamond, not a 7x7 ellipse (8 pixels differed).

## 3. Recipes
```python
# speckle removal then hole fill on a segmentation mask
m = cv2.morphologyEx(m, cv2.MORPH_OPEN,  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
# extract horizontal table lines
horiz = cv2.morphologyEx(bw, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (w // 30, 1)))
# flatten uneven illumination for thresholding (text darker than background)
bh = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25)))
```

## 4. Grayscale morphology
On grayscale, erode = local minimum filter, dilate = local maximum. Useful for background
estimation (large closing) and peak detection (`img == cv2.dilate(img, k)` → local maxima).

## Gotchas
- Polarity: operations act on **white** (non-zero). Dark objects on light background → invert
  first or swap open/close.
- Border handling: default border for erode is "max value" so edges aren't eaten; for
  dilate it's "min". Custom `borderType` can change edge behaviour.
- Large kernels are slow (cost ∝ kernel area for non-rect); rectangles are separable and fast.

## Verify
- [ ] Before/after overlays on representative masks reviewed.
- [ ] Kernel sizes expressed relative to image resolution, not hard-coded for one camera.
- [ ] Object areas after open/close stay within a few % of before (no unintended shrink).
