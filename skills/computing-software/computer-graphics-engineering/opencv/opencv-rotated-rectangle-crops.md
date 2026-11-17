---
id: computing-software.computer-graphics-engineering.opencv.opencv-rotated-rectangle-crops
name: opencv-rotated-rectangle-crops
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-contours, rotated-crop, minarearect, boxpoints, warpperspective, imgproc]
level: practitioner
status: docs-checked
description: "Crop rotated rectangles from minAreaRect in OpenCV: boxPoints corners, perspective warp vs rotate-then-getRectSubPix, and mapping crop coordinates back."
sources: ["https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html", "https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cropping rotated rectangles

`rect = cv2.minAreaRect(cnt)` returns a rotated rectangle: `((cx, cy), (w, h), angle)`.
`cv2.boxPoints(rect)` returns its four vertices.

## Angle convention
The angle range and the w/h assignment depend on the OpenCV version, and the reference page does
not pin them down. Do not hard-code assumptions: derive orientation from the box points.

## Crop via perspective warp
```python
def crop_rotated(img, rect):
    (cx, cy), (w, h), a = rect
    if w < h:                                   # make the output landscape
        w, h = h, w; a -= 90
    box = cv2.boxPoints(((cx, cy), (w, h), a)).astype(np.float32)
    # order the 4 corners yourself so they pair with dst (check by drawing them)
    dst = np.float32([[0, h - 1], [0, 0], [w - 1, 0], [w - 1, h - 1]])
    M = cv2.getPerspectiveTransform(box, dst)
    return cv2.warpPerspective(img, M, (int(w), int(h)), flags=cv2.INTER_CUBIC), M
```
Using the 4 corners avoids rotating the whole image; the warp is only right when the corner order
in `box` matches `dst`.

## Alternative: rotate then slice
```python
M = cv2.getRotationMatrix2D((cx, cy), a, 1.0)
rot = cv2.warpAffine(img, M, img.shape[1::-1])
crop = cv2.getRectSubPix(rot, (int(w), int(h)), (cx, cy))
```
`getRectSubPix` retrieves a pixel rectangle with sub-pixel accuracy. Rotating the full image costs
more than warping only the box and can clip corners unless the canvas is enlarged.

## Mapping back
Points in the crop map to the image with `cv2.perspectiveTransform(pts, np.linalg.inv(M))`.

## Verify
Draw `boxPoints` on the source and confirm the crop shows the same content upright; test
rectangles at several angles including near-axis-aligned ones.

## Checked
2026-11-01. Confirmed in the OpenCV 4.x shape reference (minAreaRect, boxPoints: four vertices of a
rotated rect) and transform reference (getRectSubPix: sub-pixel rectangle; warpAffine,
warpPerspective, perspectiveTransform exist). Removed: the claimed 4.5.1 angle-range change, the
boxPoints corner-order claim, the OCR rotation advice and specific test angles; neither page states
them.
Method: documentation only; no commands were run.
