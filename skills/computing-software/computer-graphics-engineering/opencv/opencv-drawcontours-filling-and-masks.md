---
id: computing-software.computer-graphics-engineering.opencv.opencv-drawcontours-filling-and-masks
name: opencv-drawcontours-filling-and-masks
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-contours, drawcontours, contour-mask, fillpoly, hierarchy, imgproc]
level: practitioner
status: docs-checked
description: "Use cv2.drawContours to fill shapes, build binary masks, handle holes via the even-odd rule, measure mean colour inside a contour and avoid contourIdx traps."
sources: ["https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html", "https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# drawContours: filling and masks

`cv2.drawContours(image, contours, contourIdx, color, thickness, lineType, hierarchy, maxLevel, offset)`

## Masks from contours
```python
cnts, hier = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros(binary.shape, np.uint8)
cv2.drawContours(mask, cnts, i, 255, thickness=cv2.FILLED)       # one contour, filled
mean_bgr = cv2.mean(img, mask=mask)[:3]
area_px = cv2.countNonZero(mask)
```
- A negative `thickness` (such as `cv2.FILLED`) draws the contour interiors. A negative
  `contourIdx` draws all contours.
- `contours` is a list of point arrays: pass `[cnt]` for one contour.

## Holes
With `thickness=FILLED` the function handles connected components with holes correctly even
without hierarchy, by analysing all outlines together with the even-odd rule. This can give
wrong results for a joint collection of separately retrieved contours. The docs' fix: call
`drawContours` separately for each sub-group of contours, or iterate with `contourIdx`.
- `hierarchy` is only needed to draw some of the contours; `maxLevel` 0 draws only the
  specified contour, 1 adds its nested contours, and so on (ignored without hierarchy).
- `fillPoly` also fills areas with holes and self-intersections; build one call per component.
- Use `offset=(dx, dy)` to shift all drawn contours.

## Gotchas
- `contourArea` uses Green's formula, so it and the pixel count of a mask drawn with
  `drawContours` or `fillPoly` can differ. Report one consistently.
- `contourArea` gives wrong results for contours with self-intersections.
- Draw on a copy if you need the original; `drawContours` writes into `image`.

## Verify
Draw a filled contour of a known shape on a blank mask and compare `countNonZero` with the area
you expect; check a shape with a hole is empty inside.

## Checked
2026-11-01. Confirmed in the OpenCV 4.x imgproc draw reference (drawContours parameters and the
FILLED even-odd note; fillPoly) and the shape reference (contourArea: Green's formula, differs from
pixel count, self-intersections). Corrected: the old claim that filling an outer contour fills its
holes (the docs say FILLED handles holes via even-odd). Removed: the bare-array "dots" claim, int32
(N,1,2) point shapes, LINE_AA advice and the exact rectangle pixel-count formula.
Method: documentation only; no commands were run.
