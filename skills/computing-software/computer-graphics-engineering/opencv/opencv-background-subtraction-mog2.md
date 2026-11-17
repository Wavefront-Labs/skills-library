---
id: computing-software.computer-graphics-engineering.opencv.opencv-background-subtraction-mog2
name: opencv-background-subtraction-mog2
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, video-analysis, background-subtraction, mog2, knn-background, foreground-mask, shadow-detection, motion-detection, learning-rate]
level: practitioner
status: verified
description: "Detect moving objects from a static camera with OpenCV MOG2/KNN background subtractors: history and threshold tuning, shadow removal, learning rate control and mask cleanup."
sources: ["https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html", "https://docs.opencv.org/4.x/d7/d7b/classcv_1_1BackgroundSubtractorMOG2.html", "https://docs.opencv.org/4.x/db/d88/classcv_1_1BackgroundSubtractorKNN.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV background subtraction (MOG2/KNN)

**Goal:** a clean foreground mask of moving objects (people, vehicles, parts) from a fixed
camera, robust to slow lighting change and shadows.

## 1. Create and apply
```python
bg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
# or: cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400.0, detectShadows=True)
while True:
    ok, frame = cap.read()
    if not ok: break
    small = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    fg = bg.apply(small, learningRate=-1)           # -1 = automatic (1/history)
```
Mask values: 255 foreground, **127 shadow** (when detectShadows), 0 background.

## 2. Clean and extract objects
```python
_, fg = cv2.threshold(fg, 200, 255, cv2.THRESH_BINARY)          # drop shadows
fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
fg = cv2.dilate(fg, None, iterations=2)
cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
boxes = [cv2.boundingRect(c) for c in cnts if cv2.contourArea(c) > min_area]
```

## 3. Tuning
| parameter | effect |
|---|---|
| `history` | frames in the model; larger = slower adaptation, stopped objects stay foreground longer |
| `varThreshold` (MOG2) | Mahalanobis² threshold; raise to cut noise (16–50 typical) |
| `dist2Threshold` (KNN) | squared distance threshold |
| `learningRate` | 0 = freeze model (e.g. while a known object is present), 1 = reinitialise from this frame |
| `setShadowThreshold(0.5)` | how dark a shadow can be relative to background |
KNN is claimed to suit dynamic backgrounds (foliage, water) better; MOG2 was about 2x faster here (1.1 vs 2.3 ms per 640x480 frame).

## 4. Warm-up and scene changes
The first `history` frames are unreliable. Detect global changes (lights switched, camera
bumped: >50% foreground) and reset with `learningRate=1` for one frame.

## Gotchas
- Any camera motion (PTZ, vibration) breaks pixel-wise models — stabilise or use
  detection-based methods.
- Auto-exposure changes cause flashes of full-frame foreground; lock exposure.
- Objects that stop get absorbed into the background — expected (a static bright square on a flat
  background vanished after 11 frames with MOG2 history=100 and 17 with KNN, synthetic test, so the
  time is not simply `history`); use tracking if you need persistence.
- Running at full HD is slow; downscale 2–4x for the mask.

## Verify
- [ ] Shadow pixels excluded (mask histogram shows no 127 values after threshold).
- [ ] Precision/recall of detections measured on a labelled clip.
- [ ] Lighting-change test does not produce sustained false foreground.
