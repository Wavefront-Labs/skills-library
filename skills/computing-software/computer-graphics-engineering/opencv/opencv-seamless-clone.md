---
id: computing-software.computer-graphics-engineering.opencv.opencv-seamless-clone
name: opencv-seamless-clone
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-photo, seamlessclone, poisson-blending, mixed-clone, image-compositing]
level: practitioner
status: docs-checked
description: "Composite objects into images with cv::seamlessClone (Poisson blending): NORMAL vs MIXED clone, mask prep, centre placement and failure modes."
sources: ["https://docs.opencv.org/4.x/df/da0/group__photo__clone.html", "https://github.com/opencv/opencv/blob/4.x/modules/photo/include/opencv2/photo.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seamless cloning (Poisson blending)

## 1. Call
```python
mask = np.zeros(src.shape[:2], np.uint8)
cv2.fillPoly(mask, [poly], 255)                  # region of src to transplant
center = (dst_x, dst_y)                          # where the centre of src is placed in dst
out = cv2.seamlessClone(src, dst, mask, center, cv2.NORMAL_CLONE)
```
The point `p` is where the centre of the `src` image is placed in `dst`. `src` and `dst` must be 8-bit 3-channel; the mask is
8-bit with 1, 3 or 4 channels, non-zero marks the region to blend, and an empty Mat blends the whole of `src`. The result has
the size and type of `dst`.

## 2. Modes
| Flag | Effect |
|---|---|
| `NORMAL_CLONE` (1) | Inserts objects with complex outlines, preserving the object's appearance and lighting |
| `MIXED_CLONE` (2) | Combines structure from the source with texture from the destination; works with loosely defined selections |
| `MONOCHROME_TRANSFER` (3) | Replaces features such as grayscale textures or patterns |
`NORMAL_CLONE_WIDE` (9), `MIXED_CLONE_WIDE` (10) and `MONOCHROME_TRANSFER_WIDE` (11) use an advanced ROI calculation.
Related: `colorChange`, `illuminationChange`, `textureFlattening`.

## 3. Mask preparation
- Try a mask with a margin of background around the object, and compare against one hugging the silhouette.
- Keep the placed region inside `dst`; the header does not describe out-of-bounds behaviour, so test it.

## Gotchas
- Colours can shift toward the destination; use alpha compositing if exact colour matters.
- Source and destination must both be 8-bit 3-channel.

## Verify
- [ ] No visible seam at the mask border at 100 percent zoom.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/photo/include/opencv2/photo.hpp. Confirmed: seamlessClone signature and parameter semantics (p is the centre of src), SeamlessCloneFlags values including the WIDE variants, 8-bit 3-channel requirement. Fixed the centre-of-mask claim; removed the unconfirmed exception and speed statements.
Method: documentation only; no commands were run.
