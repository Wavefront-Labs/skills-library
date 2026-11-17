---
id: computing-software.computer-graphics-engineering.opencv.opencv-otsu-and-adaptive-thresholding
name: opencv-otsu-and-adaptive-thresholding
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, thresholding, otsu, adaptive-threshold, binarization, document-scanning, triangle-threshold, uneven-illumination]
level: practitioner
status: verified
description: "Binarise images in OpenCV: global threshold types, Otsu and triangle automatic thresholds, adaptiveThreshold for uneven lighting, and CLAHE/background normalisation first."
sources: ["https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html", "https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html", "https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV Otsu and adaptive thresholding

**Goal:** clean black/white masks from grayscale images — documents, parts on a conveyor,
blobs — without hand-tuning a magic number per image.

## 1. Global threshold
```python
_, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)       # or _INV, TRUNC, TOZERO
```
Fine only for controlled lighting (backlit parts, lightbox).

## 2. Otsu (bimodal histograms)
```python
blur = cv2.GaussianBlur(gray, (5, 5), 0)                        # Otsu is noise-sensitive
t, bw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print("chosen threshold", t)
```
Otsu picks the threshold that minimises intra-class variance — works when foreground and
background form two histogram peaks. `THRESH_TRIANGLE` suits one dominant peak with a long
tail (small bright objects on large dark background). `THRESH_TRIANGLE` requires 8-bit single-channel input; `THRESH_OTSU` also accepted a uint16 image on 4.14.0 and 5.0.0
(it returned 19000 for data scaled by 200), but not 3-channel input (error).

## 3. Adaptive (uneven illumination)
```python
bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                           cv2.THRESH_BINARY, blockSize=31, C=10)
```
- Threshold per pixel = (Gaussian-weighted or mean) neighbourhood value − C.
- `blockSize` (odd) should exceed the stroke/object width — ~2–3x the text height for documents.
- `C` raises the bar: larger C → less noise in flat regions, thinner strokes.
- Flat regions produce noise; follow with morphology open or a minimum-area filter.

## 4. Normalise illumination first (often better than adaptive)
```python
bg = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51, 51)))
norm = cv2.divide(gray, bg, scale=255)                           # flatten shading
_, bw = cv2.threshold(norm, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```
Or `cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)` to boost local contrast
before thresholding (CLAHE limits the noise amplification of plain `equalizeHist`).

## Gotchas
- Thresholding colour images: convert to gray or pick the most discriminative channel
  (often a Lab or HSV channel) — `threshold` on BGR thresholds each channel independently.
- Otsu on a unimodal histogram (empty scene) still returns *a* threshold (Gaussian noise around 100 gave 99 and a 51% foreground
  fraction) — validate with the fraction of foreground pixels.
- `adaptiveThreshold` only supports 8-bit input (uint16 raises an error); scale 16-bit data first. `blockSize` must be odd (30 raised an error).
  The per-pixel rule `src > local_mean - C` (box mean or Gaussian-weighted mean) matched 99% of pixels in a NumPy/`boxFilter` re-implementation.

## Verify
- [ ] Test set with shadows/gradients: chosen method produces masks with stable foreground fraction.
- [ ] Logged Otsu threshold values stay in an expected band in production.
- [ ] Downstream (OCR, contour count) metrics compared across methods before choosing.
