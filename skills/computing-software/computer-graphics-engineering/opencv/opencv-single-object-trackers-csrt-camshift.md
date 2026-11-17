---
id: computing-software.computer-graphics-engineering.opencv.opencv-single-object-trackers-csrt-camshift
name: opencv-single-object-trackers-csrt-camshift
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-video, csrt, camshift, kcf, object-tracking, meanshift]
level: practitioner
status: docs-checked
description: "Track one object in OpenCV with the Tracker API (CSRT, KCF, MIL, Nano, Vit) or CamShift and meanShift on a histogram back projection."
sources: ["https://raw.githubusercontent.com/opencv/opencv/4.x/modules/video/include/opencv2/video/tracking.hpp", "https://raw.githubusercontent.com/opencv/opencv_contrib/4.x/modules/tracking/include/opencv2/tracking.hpp", "https://raw.githubusercontent.com/opencv/opencv/4.x/doc/tutorials/others/meanshift.markdown", "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/python/tutorial_code/video/meanshift/camshift.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-object trackers

## 1. Tracker API
Base class `cv::Tracker` (video/tracking.hpp): `init(image, boundingBox)` starts tracking from a known box; `update(image, boundingBox)` returns true if the target was located (box updated), false if the tracker cannot locate it. The header notes false does not imply tracker failure: the target may genuinely be out of the frame.
```python
tr = cv2.TrackerCSRT_create()      # CSRT lives in opencv_contrib's tracking module
tr.init(frame, (x, y, w, h))
ok, box = tr.update(next_frame)
```
Implementations in the headers read:
- `TrackerMIL`: online-trained classifier separating object from background; Multiple Instance Learning is meant to avoid drift (core video module).
- `TrackerCSRT` (contrib): Discriminative Correlation Filter with Channel and Spatial Reliability; `Params` include use_hog, use_color_names, use_gray, use_rgb, use_channel_weights, use_segmentation and window function; `setInitialMask(mask)` exists.
- `TrackerKCF` (contrib): Kernelized Correlation Filter, based on circulant-matrix properties for speed, with a colour-names extension; `Params` include desc_pca and desc_npca.
- `TrackerNano`: needs two models (backbone and neckhead) passed via `Params` or as pre-loaded `dnn::Net`; `getTrackingScore()` returns a score.
- `TrackerVit`: lightweight dnn tracker (model file about 767 KB); `Params` have the net path, backend, target, mean, std and `tracking_score_threshold` (the pre-loaded-model constructor defaults to 0.20); `getTrackingScore()`.
- `TrackerGOTURN` and `TrackerDaSiamRPN` also exist in the video module. Older trackers sit in the contrib "Legacy Tracking API" group.

## 2. meanShift and CamShift on a back projection
- `meanShift(probImage, window, criteria)` moves the window to the mass centre of the back projection until `criteria.maxCount` iterations or a shift below `criteria.epsilon`; window size and orientation do not change. The header suggests pre-filtering a noisy back projection (for example findContours, drop small contourArea, drawContours the rest).
- `CamShift(probImage, window, criteria)` finds the centre with meanShift, then adjusts window size and finds the optimal rotation; it returns a `RotatedRect`, and `boundingRect()` of it gives the next search window. Tutorial: size is updated as s = 2 * sqrt(M00 / 256).
- The tutorial sample builds a hue-only histogram of the target ROI, masking out low-light pixels with `inRange`:
```python
roi_hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
dst = cv.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
ret, track_window = cv.CamShift(dst, track_window, term_crit)
pts = cv.boxPoints(ret)
```

## Verify
- [ ] Compare tracker boxes with ground-truth boxes on recorded clips to see drift (practitioner guidance).

## Checked
Method: docs-checked 2026-11-09 against video/tracking.hpp (4.x), opencv_contrib tracking.hpp (CSRT and KCF sections), the meanshift tutorial markdown and the camshift.py sample, raw GitHub; docs.opencv.org was not readable.
Removed as unconfirmed: CSRT fps figure, KCF "no scale change", the tracker-choice table, the claim that Boosting, MedianFlow, TLD and MOSSE live in cv2.legacy (only a legacy group is named), "works only when target colour differs from background", detector-every-N-frames advice, init-box tightness and thread-safety notes.
