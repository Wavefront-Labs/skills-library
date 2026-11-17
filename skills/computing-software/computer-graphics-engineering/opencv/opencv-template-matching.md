---
id: computing-software.computer-graphics-engineering.opencv.opencv-template-matching
name: opencv-template-matching
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, objdetect, template-matching, matchtemplate, tm-ccoeff-normed, multi-scale-matching, non-maximum-suppression, masked-template, minmaxloc]
level: practitioner
status: verified
description: "Find known patterns with OpenCV matchTemplate: choosing the comparison method, thresholds, multiple matches with NMS, multi-scale/rotation search, masks."
sources: ["https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html", "https://docs.opencv.org/4.x/df/dfb/group__imgproc__object.html", "https://docs.opencv.org/4.x/de/da9/tutorial_template_matching.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenCV template matching

**Goal:** locate fixed-appearance patterns — UI elements in screenshots, fiducials, logos,
parts in a fixture — quickly and with a meaningful confidence score.

## 1. Basic match
```python
res = cv2.matchTemplate(img_gray, tmpl_gray, cv2.TM_CCOEFF_NORMED)   # (H-h+1, W-w+1) score map
_, max_val, _, max_loc = cv2.minMaxLoc(res)
if max_val > 0.8: x, y = max_loc; box = (x, y, w, h)
```
Methods: `TM_CCOEFF_NORMED` (zero-mean normalised correlation, robust to brightness/contrast
changes; score in [−1, 1]) is the default choice. `TM_SQDIFF(_NORMED)`: best match is the
**minimum**. Unnormalised methods give scores that can't be thresholded across images.

## 2. Multiple instances
```python
ys, xs = np.where(res >= 0.85)
boxes = [[int(x), int(y), w, h] for x, y in zip(xs, ys)]
scores = [float(res[y, x]) for x, y in zip(xs, ys)]
keep = cv2.dnn.NMSBoxes(boxes, scores, score_threshold=0.85, nms_threshold=0.3)
```
Without NMS you get clusters of overlapping hits around each true location (19 hits for 3 planted copies, 3 after `NMSBoxes`).

## 3. Scale and rotation
matchTemplate is not scale/rotation invariant. Options:
- Search a small set of scales (image pyramid or resized templates, e.g. 0.8–1.2 in 5% steps),
  keep the best normalised score.
- Rotations: rotated templates (costly) — or switch to feature matching (ORB/SIFT + homography)
  or shape-based matching for arbitrary pose.

## 4. Masks and transparency
Templates with irrelevant background (icons with transparent corners): pass `mask=alpha` (same size as the template;
`matchTemplate(img, t, method, mask=alpha)`). All six methods accepted a mask on OpenCV 4.14.0 and 5.0.0; very old
versions supported fewer, so check if you must support them.

## 5. Speed
Cost ∝ image area × template area; OpenCV uses FFT for large templates automatically. Restrict
the search ROI, downscale both images (coarse-to-fine), or use UMat/CUDA
(`cv2.cuda.createTemplateMatching`, only in CUDA builds; pip wheels do not include it).

## Gotchas
- Threshold depends on content; calibrate on positives and negatives (score histograms).
- Different rendering (anti-aliasing, DPI scaling in UI screenshots, compression) lowers scores —
  capture templates under deployment conditions.
- Flat/low-texture templates produce high scores everywhere with normalised methods (a constant template gave exactly 1.0 for
  `TM_CCOEFF_NORMED` at every position and a minimum of 0.92 for `TM_CCORR_NORMED`).
- Brightness/contrast change (x0.5 + 40) kept `TM_CCOEFF_NORMED` at 0.9999 for the right location.

## Verify
- [ ] Score threshold chosen from a positive/negative score distribution.
- [ ] Multi-instance cases deduplicated with NMS.
- [ ] Latency measured with ROI/scale limits applied.
