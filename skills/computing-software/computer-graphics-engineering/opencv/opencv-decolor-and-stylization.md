---
id: computing-software.computer-graphics-engineering.opencv.opencv-decolor-and-stylization
name: opencv-decolor-and-stylization
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-photo, decolor, stylization, pencil-sketch, non-photorealistic, photo]
level: practitioner
status: docs-checked
description: "Use OpenCV photo NPR filters: decolor contrast-preserving grayscale, stylization watercolour look, pencilSketch, and their sigma_s/sigma_r parameters and speed limits."
sources: ["https://docs.opencv.org/4.x/df/dac/group__photo__render.html", "https://docs.opencv.org/4.x/d4/d32/group__photo__decolor.html", "https://github.com/opencv/opencv/blob/4.x/modules/photo/include/opencv2/photo.hpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# decolor and stylization filters

## Contrast-preserving decolorisation
```python
gray, boost = cv2.decolor(bgr)      # gray: uint8 1-ch, boost: colour image with boosted contrast
```
- Documented as a basic tool in digital printing and stylized black-and-white rendering (reference key CL12).
  `src` must be an 8-bit 3-channel colour image; `grayscale` is 8-bit 1-channel and `color_boost` is 8-bit 3-channel.
- Judge speed and frame-to-frame consistency on your own data before using it in a video or measurement pipeline;
  the header makes no claim about either.

## Stylisation (domain transform based)
```python
out = cv2.stylization(bgr, sigma_s=60, sigma_r=0.45)
g, c = cv2.pencilSketch(bgr, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
```
- `sigma_s` (range 0 to 200) and `sigma_r` (range 0 to 1) are the documented ranges; defaults are 60 and 0.45 for
  `stylization`, and 60, 0.07 and `shade_factor` 0.02 for `pencilSketch`.
- `shade_factor` has range 0 to 0.1.
- Input must be 8-bit 3-channel. `pencilSketch` returns an 8-bit 1-channel image and a colour image the size and type of `src`.

## Performance
Time the call at your production resolution; for video, consider processing at reduced resolution.

## Verify
Compare `decolor` against `cvtColor(BGR2GRAY)` on a test chart of colours with similar luminance and check that the pattern
remains visible.

## Checked

2026-10-26, against OpenCV 4.x branch (latest tag 4.14.0, 5.0.0 also released; 4.x branch commit of 2026-10-25): modules/photo/include/opencv2/photo.hpp. Confirmed: decolor signature and 8-bit requirements, stylization and pencilSketch signatures, defaults and parameter ranges. Removed the unconfirmed speed, scaling and ximgproc statements.
Method: documentation only; no commands were run.
