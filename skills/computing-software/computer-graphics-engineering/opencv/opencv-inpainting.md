---
id: computing-software.computer-graphics-engineering.opencv.opencv-inpainting
name: opencv-inpainting
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, opencv-photo, computational-photography, inpainting, inpaint-telea, inpaint-ns, object-removal, scratch-removal, mask-dilation]
level: practitioner
status: docs-checked
description: "Remove scratches, text overlays, sensor dust and small objects with OpenCV inpaint (Telea, Navier-Stokes): building the mask, radius choice."
sources: ["https://docs.opencv.org/4.x/d7/d8b/group__photo__inpaint.html", "https://docs.opencv.org/4.x/de/daa/group__xphoto.html", "https://github.com/opencv/opencv_contrib/blob/4.x/modules/xphoto/include/opencv2/xphoto/inpainting.hpp", "https://github.com/opencv/opencv/blob/4.x/modules/photo/include/opencv2/photo.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV inpainting

**Goal:** fill small damaged or unwanted regions so the result is not noticeable at
viewing size.

## 1. Build the mask (the real work)
`cv2.inpaint` mask: 8-bit single channel, same size as `src`, **non-zero = pixels to fill** (the docs state it this way).
- Watermark/timestamp: threshold the known overlay colour, or a fixed template location.
- Thin dark scratches: `cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, k)` then threshold.
- Consider dilating the mask by a few pixels so the defect's edge pixels are also replaced.
```python
mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
```

## 2. Inpaint
```python
out_t = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)   # fast marching
out_n = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_NS)      # Navier-Stokes
```
- `src`: 8-bit, 16-bit unsigned or 32-bit float 1-channel, or 8-bit 3-channel; `dst` has the same size and type.
- `inpaintRadius` is the radius of the circular neighbourhood of each point considered by the algorithm; tune it on your data.
- The function reconstructs the area from pixels near the region boundary, so large regions across texture will not recover detail.

## 3. Larger regions
- `cv2.xphoto.inpaint(img, mask, dst, cv2.xphoto.INPAINT_SHIFTMAP)` (opencv_contrib) or `INPAINT_FSR_BEST` / `INPAINT_FSR_FAST`.
  **The xphoto mask is inverted: non-zero pixels mark the valid area and zero pixels are filled** (`CV_8UC1`).
  SHIFTMAP accepts any type with 1 to 4 channels; the FSR modes need 1-channel grayscale or 3-channel BGR.

## 4. Depth map hole filling
`cv2.inpaint` accepts 16-bit unsigned and 32-bit float 1-channel input, so a depth map can be inpainted with the missing-value
pixels as the mask. Be careful at object boundaries, where filling mixes foreground and background depths.

## Gotchas
- Any non-zero mask value counts; the mask must be single channel.
- Set expectations for textured regions, or try the xphoto methods.

## Verify
- [ ] Visual A/B at 100% zoom on a test set of defects.
- [ ] Mask overlay review: every defect covered, with margin.
- [ ] Runtime acceptable for the largest expected mask.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/photo/include/opencv2/photo.hpp and opencv_contrib modules/xphoto/include/opencv2/xphoto/inpainting.hpp (4.x). Confirmed: inpaint input types and mask, INPAINT_NS = 0 / INPAINT_TELEA = 1, xphoto algorithms and their inverted mask. Removed the unconfirmed radius, size-limit and learned-inpainting statements.
Method: documentation only; no commands were run.
