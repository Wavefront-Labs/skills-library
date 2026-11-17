---
id: computing-software.computer-graphics-engineering.opencv.opencv-copymakeborder-padding
name: opencv-copymakeborder-padding
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-geometric-transforms, copymakeborder, padding, letterbox, border-types, imgproc]
level: practitioner
status: verified
description: "Pad images in OpenCV with copyMakeBorder: border types, constant colour, letterboxing for DNN input, padding for DFT sizes and tiled processing, and undoing the padding."
sources: ["https://docs.opencv.org/4.x/d2/de8/group__core__array.html", "https://docs.opencv.org/4.x/dc/da3/tutorial_copyMakeBorder.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# copyMakeBorder padding

```python
out = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
```
Border types: `BORDER_CONSTANT`, `BORDER_REPLICATE`, `BORDER_REFLECT`, `BORDER_REFLECT_101`,
`BORDER_WRAP` (see filter2D for patterns). `value` is a per-channel scalar for CONSTANT.

## Letterboxing for detector input (YOLO-style)
```python
def letterbox(img, size=640, color=(114, 114, 114)):
    h, w = img.shape[:2]; r = min(size / h, size / w)
    nh, nw = round(h * r), round(w * r)
    img = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
    top = (size - nh) // 2; left = (size - nw) // 2
    img = cv2.copyMakeBorder(img, top, size - nh - top, left, size - nw - left,
                             cv2.BORDER_CONSTANT, value=color)
    return img, r, (left, top)
# map boxes back: x = (x_net - left) / r ; y = (y_net - top) / r
```
Keep `r` and the offsets: forgetting the offset shifts every box by half the padding.

## Padding for DFT
```python
H = cv2.getOptimalDFTSize(h); W = cv2.getOptimalDFTSize(w)
padded = cv2.copyMakeBorder(gray, 0, H - h, 0, W - w, cv2.BORDER_CONSTANT, value=0)
```
Pad bottom/right so the crop back is `out[:h, :w]`. Reflect padding reduces spectral leakage
from the image border at the cost of mirrored content.

## Tiled processing
Pad each tile by the filter radius (`BORDER_REFLECT_101` at the true image edge, real neighbour
pixels elsewhere), process, then crop the margin. For whole-image ops prefer
`cv2.copyMakeBorder` once then slicing tiles from the padded array.

## Gotchas
- With an ROI view (`img[y:y+h, x:x+w]`), C++ copyMakeBorder can use real pixels outside the ROI
  unless `BORDER_ISOLATED` is OR-ed into the type. A NumPy slice in Python did not: `BORDER_REFLECT_101`
  on a slice reflected the slice's own pixels with or without `BORDER_ISOLATED` (checked on 5.0.0).
- `value` for single-channel images: pass a scalar; a 3-tuple is accepted but only the first
  component is used (`(7, 9, 11)` gave 7).
- Padding changes coordinates: offset keypoints/boxes/camera principal point by (left, top).

## Verify
`out[top:top+h, left:left+w]` must equal the input exactly.
