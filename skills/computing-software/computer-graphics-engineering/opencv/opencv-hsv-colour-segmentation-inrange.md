---
id: computing-software.computer-graphics-engineering.opencv.opencv-hsv-colour-segmentation-inrange
name: opencv-hsv-colour-segmentation-inrange
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, colour-segmentation, thresholding, cvtcolor, inrange, hsv, lab-colour-space, red-hue-wraparound, color-mask, lighting-invariance]
level: practitioner
status: verified
description: "Segment objects by colour in OpenCV: cvtColor to HSV or Lab, OpenCV's 0-179 hue range, red hue wrap-around, inRange masks, morphology cleanup and lighting robustness."
sources: ["https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html", "https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html", "https://docs.opencv.org/4.x/da/d97/tutorial_threshold_inRange.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV HSV colour segmentation with inRange

**Goal:** a binary mask of "the orange ball" / "green screen" / "red markings" that holds up
when lighting changes.

## 1. Convert
```python
blur = cv2.GaussianBlur(bgr, (5, 5), 0)              # reduce sensor noise first
hsv  = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
```
OpenCV 8-bit HSV ranges: **H 0–179** (degrees / 2), S 0–255, V 0–255. Values copied from
GIMP/Photoshop (H 0–360, S/V 0–100) must be rescaled. `COLOR_BGR2HSV_FULL` uses H 0–255 (pure green 85, pure blue 171 vs 60 and 120 for plain `COLOR_BGR2HSV`).
Input is **BGR**: using `COLOR_RGB2HSV` on imread output swaps red and blue hues.

## 2. Threshold
```python
lower = np.array([10, 120, 80]); upper = np.array([25, 255, 255])   # orange
mask = cv2.inRange(hsv, lower, upper)                                # 255 inside, 0 outside
```
Red straddles hue 0 — use two ranges:
```python
m1 = cv2.inRange(hsv, (0, 120, 70), (10, 255, 255))
m2 = cv2.inRange(hsv, (170, 120, 70), (179, 255, 255))
mask = cv2.bitwise_or(m1, m2)
```

## 3. Clean the mask
```python
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)     # remove speckles
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)    # fill holes
cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = [c for c in cnts if cv2.contourArea(c) > 200]
```

## 4. Picking thresholds
- Sample real pixels: click on the object (mouse callback) and print HSV; take the range
  over many frames/lighting conditions, add margins.
- Low S or low V → hue is meaningless (greys, near-black): always set a minimum S and V.
- Use trackbars for live tuning, then freeze values in config.

## 5. When HSV isn't enough
- **Lab** (`COLOR_BGR2Lab`) separates lightness L from chroma a/b — thresholding a/b is often
  more stable under brightness changes than HSV.
- Normalise illumination first (white balance, CLAHE on V/L channel).
- Many similar colours / textured backgrounds: back-projection of a hue-saturation histogram
  or a small learned segmentation model.

## Gotchas
- Auto-exposure/auto white balance on webcams shifts colours over time — lock them
  (`CAP_PROP_AUTO_EXPOSURE`, `CAP_PROP_AUTO_WB`) for vision tasks.
- JPEG chroma subsampling bleeds colour at edges; masks are softer than the object.
- `inRange` bounds are inclusive and per-channel; no hue wrap-around handling.

## Verify
- [ ] Mask tested on images from at least 3 lighting conditions.
- [ ] Red-object case uses the dual-range mask.
- [ ] Thresholds stored in config with the camera settings used to derive them.
