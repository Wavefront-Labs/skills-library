---
id: computing-software.computer-graphics-engineering.opencv.opencv-detailenhance-and-edgepreservingfilter
name: opencv-detailenhance-and-edgepreservingfilter
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-photo, detailenhance, edgepreservingfilter, local-contrast, domain-transform, photo]
level: practitioner
status: docs-checked
description: "Use OpenCV photo edge-preserving filters: edgePreservingFilter (RECURS vs NORMCONV), detailEnhance for local contrast, parameter ranges, and comparison with bilateral filtering."
sources: ["https://docs.opencv.org/4.x/df/dac/group__photo__render.html", "https://github.com/opencv/opencv/blob/4.x/modules/photo/include/opencv2/photo.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Edge-preserving and detail-enhance filters

## edgePreservingFilter
```python
smooth = cv2.edgePreservingFilter(bgr, flags=cv2.RECURS_FILTER, sigma_s=60, sigma_r=0.4)
```
- `RECURS_FILTER` (1): recursive filtering. `NORMCONV_FILTER` (2): normalised convolution filtering. Compare the two on your data.
- `sigma_s` range 0 to 200, `sigma_r` range 0 to 1 (defaults 60 and 0.4). Input and output are 8-bit 3-channel.

## detailEnhance
```python
detail = cv2.detailEnhance(bgr, sigma_s=10, sigma_r=0.15)
```
- Enhances detail in the image (defaults `sigma_s` 10, `sigma_r` 0.15, same documented ranges).
- Check strong settings on noisy or heavily compressed input: they can amplify noise, so consider denoising first.

## Manual base/detail control
For finer control, one way to build it yourself (an illustrative sketch, not a documented recipe):
```python
f = bgr.astype(np.float32) / 255
base = cv2.edgePreservingFilter(bgr, flags=1, sigma_s=30, sigma_r=0.2).astype(np.float32) / 255
out = np.clip(base + 1.8 * (f - base), 0, 1)
```
Apply on luminance only (Lab L channel) to avoid colour shifts.

## When to use which
| Need | Filter |
|---|---|
| Edge-preserving smoothing | `edgePreservingFilter` |
| Bilateral semantics | `bilateralFilter` |
| Local detail boost | `detailEnhance` |

## Verify
Step-edge test image with noise: edge profile stays sharp, flat region noise standard deviation
drops.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/photo/include/opencv2/photo.hpp. Confirmed: edgePreservingFilter flags (RECURS_FILTER = 1, NORMCONV_FILTER = 2), detailEnhance and edgePreservingFilter defaults and ranges, 8-bit 3-channel input. Removed the unconfirmed speed and quality comparisons and the ximgproc row.
Method: documentation only; no commands were run.
