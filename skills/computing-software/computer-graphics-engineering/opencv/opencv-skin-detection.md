---
id: computing-software.computer-graphics-engineering.opencv.opencv-skin-detection
name: opencv-skin-detection
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, colour-segmentation, skin-detection, histogram-skin-model, illumination-robustness]
level: practitioner
status: draft
description: "Detect skin pixels in OpenCV: YCrCb/HSV rule baselines, histogram back-projection models trained on labelled data, adaptive refinement, and their bias limitations."
sources: ["https://docs.opencv.org/4.x/da/d7f/tutorial_back_projection.html", "https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html", "https://arxiv.org/abs/1708.02694"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Skin detection

Classic colour-based skin detection is a fast pre-filter (hand tracking ROIs, face-region
priors, privacy blurring), not a reliable classifier. Expect false positives on wood, sand and
warm lighting, and **uneven performance across skin tones**; validate on diverse data.

## Rule-based baseline (YCrCb)
```python
ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
mask = cv2.inRange(ycc, (0, 133, 77), (255, 173, 127))         # Chai & Ngan style CrCb box
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
```
Ignoring Y gives some robustness to brightness; fixed boxes fail under coloured lighting.

## Histogram model (better)
Train a 2D CrCb (or HS) histogram from labelled skin pixels across many people and lighting
conditions, normalise, then back-project:
```python
hist = cv2.calcHist([ycc_train], [1, 2], skin_mask_train, [64, 64], [0, 256, 0, 256])
cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
prob = cv2.calcBackProject([ycc], [1, 2], hist, [0, 256, 0, 256], 1)
prob = cv2.GaussianBlur(prob, (5, 5), 0)
_, mask = cv2.threshold(prob, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```
A Bayesian variant uses a skin and a non-skin histogram and thresholds the likelihood ratio.

## Adaptive refinement
- Seed from a detected face (`FaceDetectorYN`): sample skin colour from the face region of *this*
  person/lighting, build the histogram on the fly, then detect hands/arms. Much more robust than global rules.
- Colour constancy / white balance before detection.

## When to use a network instead
Segmentation models (e.g. person/body-part segmentation, MediaPipe selfie segmentation, hand
landmark models) are far more accurate and less biased; colour rules remain useful on tiny
devices or as a cheap gate.

## Gotchas
- JPEG artefacts and chroma subsampling produce blotchy masks; smooth the probability map first.
- Thresholds tuned on one camera do not transfer; re-tune per sensor.

## Verify
- [ ] Precision/recall measured on a labelled set spanning skin tones and lighting; report per-group metrics, not just the average.
