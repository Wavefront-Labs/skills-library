---
id: computing-software.computer-graphics-engineering.opencv.opencv-clahe-and-histogram-equalization
name: opencv-clahe-and-histogram-equalization
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, colour-segmentation, clahe, histogram-equalization, equalizehist, createclahe, contrast-enhancement, lab-l-channel, low-contrast-images]
level: practitioner
status: verified
description: "Improve contrast with OpenCV: global equalizeHist vs CLAHE, choosing clipLimit and tile size, applying to colour images via the L channel."
sources: ["https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html", "https://docs.opencv.org/4.x/d6/db6/classcv_1_1CLAHE.html", "https://docs.opencv.org/4.x/d6/dc7/group__imgproc__hist.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV CLAHE and histogram equalisation

**Goal:** reveal detail in dark, hazy or low-contrast images (inspection, medical, night
footage, OCR prep) without blowing out noise.

## 1. Global equalisation
```python
eq = cv2.equalizeHist(gray)          # 8-bit single channel only
```
Spreads the global histogram to the full range. Works for uniformly low-contrast images; fails
when the image has both bright and dark regions (over-enhances large uniform areas, washes
out others).

## 2. CLAHE (contrast-limited adaptive)
```python
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
out = clahe.apply(gray)              # 8-bit or 16-bit single channel
```
- Equalises per tile with bilinear blending between tiles → local contrast.
- `clipLimit` caps each histogram bin (relative to average) before equalisation — limits noise
  amplification in flat regions. 1.5–3 typical; higher = stronger, noisier.
- `tileGridSize`: more tiles = more local (and more artefacts/halo risk); scale with image size
  and feature size (8x8 for ~1 MP).
- Reuse the CLAHE object across frames; it's cheap (1.5 ms per 1920x1080 8-bit frame measured). The
  constructor defaults are `clipLimit=40.0`, `tileGridSize=(8, 8)`, so always pass `clipLimit` explicitly.

## 3. Colour images
Never equalise B, G, R independently (colour shifts). Convert and enhance lightness only:
```python
lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)
lab = cv2.merge((clahe.apply(l), a, b))
out = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
```
(HSV V channel or YCrCb Y also work.)

## 4. When not to use it
- Measurement of intensities/radiometry: equalisation destroys the intensity mapping.
- Before algorithms tuned on natural images (some detectors) — check task metrics; it can hurt.
- Heavy sensor noise: denoise first (or lower clipLimit).

## Gotchas
- `equalizeHist` rejects 16-bit images; CLAHE accepts 16-bit (uint16 in, uint16 out) but not 3-channel input (both raise errors, checked).
- Tile boundaries can show as faint grids with high clipLimit on smooth gradients.
- Video: per-frame CLAHE is temporally stable enough usually; global equalisation flickers when
  scene content changes.

## Verify
- [ ] Before/after on representative images; noise in flat regions acceptable.
- [ ] Downstream metric (OCR CER, detection recall) compared with and without enhancement.
- [ ] Colour images processed via L/Y channel only.
