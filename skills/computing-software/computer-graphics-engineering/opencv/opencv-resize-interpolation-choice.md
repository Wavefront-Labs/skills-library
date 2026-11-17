---
id: computing-software.computer-graphics-engineering.opencv.opencv-resize-interpolation-choice
name: opencv-resize-interpolation-choice
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, geometric-transforms, cv-resize, inter-area, inter-linear, inter-cubic, inter-lanczos4, inter-nearest, aliasing, letterbox, aspect-ratio]
level: practitioner
status: verified
description: "Choose OpenCV resize interpolation by direction and content: INTER_AREA for shrinking, cubic/Lanczos for enlarging, NEAREST for masks and labels."
sources: ["https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#ga47a974309e9102f5f08231edc7e7529d", "https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#ga5bb5a1fea74ea38e1a5445ca803ff121"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV resize: choosing interpolation

**Goal:** resized images that are free of aliasing when shrinking, sharp when enlarging,
and never corrupt label maps.

## 1. Decision table
| case | flag | why |
|---|---|---|
| downscale photos/frames | `INTER_AREA` | pixel-area averaging = proper low-pass; no moire |
| upscale photos | `INTER_CUBIC` (quality) / `INTER_LINEAR` (speed) | smooth |
| upscale, max sharpness | `INTER_LANCZOS4` | sharper, can ring on edges, slowest |
| masks, segmentation labels, class IDs | `INTER_NEAREST` (or `INTER_NEAREST_EXACT`) | never invents new label values |
| depth maps | `INTER_NEAREST` across depth edges, or edge-aware | linear blends foreground/background into floating pixels |
| real-time video, any direction | `INTER_LINEAR` | default, fast |
```python
small = cv2.resize(img, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
mask_s = cv2.resize(mask, (w // 4, h // 4), interpolation=cv2.INTER_NEAREST)
```
`INTER_LINEAR` downscaling by more than 2x samples only a few source pixels per output →
aliasing (jaggies, moire on fabric/screens): 1-pixel stripes at period 9 shrunk 4x kept a row std of 31.8 with `INTER_AREA`
but 54.1 with `INTER_LINEAR` (mean 28.8 vs 29.9, true 28.7). Pyramids (`pyrDown` repeatedly) are an
alternative for power-of-two reductions.

## 2. Size vs scale factors
`cv2.resize(img, (W, H))` — **width first**. Or `cv2.resize(img, None, fx=0.5, fy=0.5)`.
Rounding: with fx/fy the output size is `round(w*fx)`; compute explicitly when you need
exact sizes (e.g. model inputs).

## 3. Aspect-preserving letterbox (model inputs)
```python
def letterbox(img, size=640, color=(114, 114, 114)):
    h, w = img.shape[:2]; r = min(size / h, size / w)
    nw, nh = round(w * r), round(h * r)
    interp = cv2.INTER_AREA if r < 1 else cv2.INTER_LINEAR
    out = cv2.copyMakeBorder(cv2.resize(img, (nw, nh), interpolation=interp),
                             (size - nh) // 2, size - nh - (size - nh) // 2,
                             (size - nw) // 2, size - nw - (size - nw) // 2,
                             cv2.BORDER_CONSTANT, value=color)
    return out, r, ((size - nw) // 2, (size - nh) // 2)    # keep r and pad to map boxes back
```
Training and inference must use identical resize and padding.

## Gotchas
- Pixel-centre convention: OpenCV maps pixel centres (x+0.5); other libraries (PIL, torch
  `align_corners=True`) differ slightly — small but real accuracy differences in models.
- `INTER_AREA` for an integer upscale factor gave plain 2x2 blocks (nearest-like) in 5.0.0; don't use it to enlarge.
- A 20x20 label image with 5 values resized to 7x7 kept 5 values with `INTER_NEAREST` and `INTER_NEAREST_EXACT`, but had 24 with
  `INTER_LINEAR` and 23 with `INTER_AREA`.
- Resizing 16-bit/float images is supported; resizing `bool` NumPy arrays is not (cast to uint8) — checked.

## Verify
- [ ] Downscaled test chart (fine stripes) shows no moire.
- [ ] Resized label masks contain only valid class IDs (`np.unique` check).
- [ ] Model preprocessing identical between training and serving (bitwise compare on a sample).
