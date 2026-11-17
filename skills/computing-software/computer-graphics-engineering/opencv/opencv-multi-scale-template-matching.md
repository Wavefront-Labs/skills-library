---
id: computing-software.computer-graphics-engineering.opencv.opencv-multi-scale-template-matching
name: opencv-multi-scale-template-matching
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-objdetect, multi-scale-template-matching, matchtemplate, rotation-invariant, image-pyramid]
level: practitioner
status: docs-checked
description: "Make OpenCV template matching scale- and rotation-tolerant: image pyramids, scale sweeps, rotated templates, masked matchTemplate, NMS over hits and when to switch to features."
sources: ["https://docs.opencv.org/4.x/df/dfb/group__imgproc__object.html", "https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-scale and rotation-invariant template matching

`matchTemplate` is translation-only. Scale and rotation must be swept explicitly.

## Scale sweep
```python
best = None
for s in np.linspace(0.5, 1.5, 21):
    t = cv2.resize(tmpl, None, fx=s, fy=s, interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR)
    if t.shape[0] > img.shape[0] or t.shape[1] > img.shape[1]: continue
    r = cv2.matchTemplate(img, t, cv2.TM_CCOEFF_NORMED)
    _, mx, _, loc = cv2.minMaxLoc(r)
    if best is None or mx > best[0]: best = (mx, loc, s)
```
Use a normalised method (`TM_*_NORMED`) when comparing scores across scales; the reference gives the normalised formulas.

## Rotation sweep
Rotate the template with `getRotationMatrix2D` + `warpAffine` in steps (5 to 10 degrees) and
match with a **mask** so the rotated corners do not contribute:
```python
r = cv2.matchTemplate(img, rot_t, cv2.TM_CCORR_NORMED, mask=rot_mask)
```
The `matchTemplate` reference gives masked formulas for `TM_SQDIFF`, `TM_SQDIFF_NORMED`, `TM_CCORR` and `TM_CCORR_NORMED`.

## Coarse-to-fine
Match at 1/4 resolution over the full sweep, then refine scale/angle at full resolution only
around the top candidates.

## Multiple instances
Threshold the score map, then non-max-suppress: dilate the score map and keep points equal to
the dilated value, or `cv2.dnn.NMSBoxes(boxes, scores, 0.8, 0.3)`.

## Subpixel location
Fit a parabola to the 3x3 neighbourhood of the peak in each axis.

## When to stop using templates
Perspective change, large scale range, occlusion, or lighting change: use feature matching
(ORB/SIFT + homography) or a trained detector. Templates are best for fixed-camera inspection.

## Verify
Synthesize test images by placing the template at known scale/angle: recovered values within one
sweep step and position within 1 px.

## Checked
Checked 2026-10-28 against OpenCV 4.13.0 docs: imgproc object detection group (matchTemplate, TemplateMatchModes) and the Python template matching tutorial; `cv::dnn::NMSBoxes` signature from the dnn group page.
- Confirmed: `TM_*` enum values and normalised variants, optional `mask` argument and masked formulas for the SQDIFF and CCORR methods, `NMSBoxes(bboxes, scores, score_threshold, nms_threshold)`.
- Removed: cross-scale score comparability claim as stated, CCOEFF mask support, the 10 to 50x speed-up.
- Sweep ranges, step sizes and the parabola fit are advice, not documentation claims.

Method: documentation only; no commands were run.
