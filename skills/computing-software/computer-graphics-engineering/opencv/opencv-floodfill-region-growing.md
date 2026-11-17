---
id: computing-software.computer-graphics-engineering.opencv.opencv-floodfill-region-growing
name: opencv-floodfill-region-growing
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, colour-segmentation, floodfill, region-growing, magic-wand]
level: practitioner
status: verified
description: "Use cv::floodFill for region growing and magic-wand selection: loDiff/upDiff, fixed vs floating range, mask mode with 2-pixel border, connectivity, and hole filling."
sources: ["https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#ga366aae45a6c1289b341d140839f18717", "https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html", "https://github.com/opencv/opencv/blob/4.x/samples/python/floodfill.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# floodFill region growing

## Magic-wand selection (mask mode)
```python
h, w = img.shape[:2]
mask = np.zeros((h + 2, w + 2), np.uint8)              # MUST be 2 px larger than the image
flags = 4 | cv2.FLOODFILL_FIXED_RANGE | cv2.FLOODFILL_MASK_ONLY | (255 << 8)
lo = up = (20, 20, 20)                                  # per-channel tolerance
cv2.floodFill(img, mask, seedPoint=(x, y), newVal=0, loDiff=lo, upDiff=up, flags=flags)
selection = mask[1:-1, 1:-1]                            # 255 where filled
```
- Low byte of `flags`: connectivity 4 or 8.
- Bits 8-15: value written into the mask (`255 << 8`).
- `FLOODFILL_FIXED_RANGE`: compare each pixel to the **seed** colour; without it, neighbours are
  compared to each other (floating range), which can leak along gradients (a 0-198 ramp with tolerance 5: 30 px filled fixed, all 1000 floating).
- `FLOODFILL_MASK_ONLY`: don't modify the image, only the mask.

## Mask as a barrier
Non-zero mask pixels are never filled: draw edges (e.g. `Canny` output, dilated) into the mask
before filling to stop leaks through weak boundaries.
```python
edges = cv2.Canny(gray, 50, 150)
mask[1:-1, 1:-1] = cv2.dilate(edges, None)
```

## Hole filling in binary masks
```python
inv = mask_bin.copy()
ff = np.zeros((h + 2, w + 2), np.uint8)
cv2.floodFill(inv, ff, (0, 0), 255)                    # fill background from a corner
holes = cv2.bitwise_not(inv)
filled = mask_bin | holes
```
Requires the corner to be background; otherwise seed from a known background pixel.

## Return values
`retval, image, mask, rect = cv2.floodFill(...)`: `retval` = number of pixels filled, `rect` =
bounding box of the filled region (handy to crop).

## Gotchas
- Wrong mask size raises an assertion; mask must be `CV_8UC1` (an `(h, w)` uint8 mask and an `(h+2, w+2)` float32 mask both raised, checked).
- A barrier drawn into the mask blocked the fill completely (a one-pixel column gave 0 filled pixels on the far side).
- Tolerances are absolute per channel in the image's colour space; Lab or HSV inputs give more
  perceptual behaviour than BGR.
- Large fills on 4K images are fast (scanline algorithm) but repeated calls per click in Python
  should reuse the mask buffer.

## Verify
- [ ] Selection matches user expectation on textured and gradient regions; hole filling leaves outer background untouched.
