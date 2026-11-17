---
id: computing-software.computer-graphics-engineering.opencv.opencv-lab-and-ycrcb-segmentation
name: opencv-lab-and-ycrcb-segmentation
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, colour-segmentation, lab-color-space, ycrcb, delta-e-segmentation]
level: practitioner
status: docs-checked
description: "Segment by colour in OpenCV using Lab and YCrCb: 8-bit scaling of L*a*b* and YCrCb, chroma-only thresholds and Delta E distance masks."
sources: ["https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html", "https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html", "https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lab and YCrCb colour segmentation

Lab and YCrCb separate lightness from chroma, so you can threshold chroma and tolerate shading.

## Value ranges in OpenCV
| Space | 8-bit encoding | float32 |
|---|---|---|
| Lab (`COLOR_BGR2Lab`) | L = L*x255/100; a = a*+128; b = b*+128 | L 0..100, a and b about -127..127 (left as is) |
| YCrCb (`COLOR_BGR2YCrCb`) | Cr and Cb offset by delta = 128 | delta = 0.5 |
- Lab conversions are listed for 8-bit and 32-bit float inputs; 16-bit is not supported.
- `COLOR_LBGR2Lab` and `COLOR_Lab2LBGR` exist as separate codes alongside `COLOR_BGR2Lab`; check the
  colour conversion page before choosing which one matches your data.
- For YCrCb the docs give `Y = 0.299R + 0.587G + 0.114B`, `Cr = (R-Y)*0.713 + delta`,
  `Cb = (B-Y)*0.564 + delta`.
- Use the same depth and conversion code when you pick thresholds and when you run the pipeline.

## Chroma-only threshold
```python
lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
L, a, b = cv2.split(lab)
mask = cv2.inRange(lab, (20, 150, 150), (255, 200, 200))   # span L widely, threshold a and b
```
Spanning L widely makes the mask depend mainly on chroma.

## Distance-to-reference mask (Delta E)
```python
labf = cv2.cvtColor(img.astype(np.float32) / 255.0, cv2.COLOR_BGR2Lab)
ref = np.array([55.0, 40.0, 30.0], np.float32)                 # target L*a*b*
dE = np.linalg.norm(labf - ref, axis=2)                         # CIE76 distance
mask = (dE < 12).astype(np.uint8) * 255
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
```
Tune the threshold on your own images; CIEDE2000 is a more elaborate distance if CIE76 is not
enough.

## Verify
- [ ] Mask stable across lit/shadowed regions of the same object (IoU vs. hand labels on varied lighting).

## Checked
2026-11-01. Confirmed in the OpenCV 4.x colour conversion pages: Lab 8-bit and float scaling,
supported depths, existence of the LBGR codes, YCrCb formulas and delta. Removed: HSV hue
instability remarks, "float32 gives accurate Lab", the sRGB-linearisation and D65 claim for BGR2Lab,
the skin-colour Cr/Cb ranges, the weighted Delta E formula, the white balance and JPEG subsampling
notes, and the 12 and range thresholds as recommendations (kept as example values only).
Method: documentation only; no commands were run.
