---
id: computing-software.computer-graphics-engineering.computer-vision.focus-stacking
name: focus-stacking
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, comp-photo-cv, focus-stacking, extended-depth-of-field, laplacian-pyramid, image-fusion, macro-photography]
level: practitioner
status: gated
description: "Merge a focus bracket into an all-in-focus image: alignment and magnification correction, per-pixel sharpness maps, Laplacian pyramid fusion, halo control and depth maps."
sources: ["https://enblend.sourceforge.io/", "https://docs.opencv.org/4.x/d3/db7/tutorial_hdr_imaging.html", "https://szeliski.org/Book/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Focus stacking

## 1. Capture
Fixed camera, constant exposure and white balance, focus steps so adjacent slices' depths of field
overlap (about 30 percent).

## 2. Align
Focus breathing changes magnification between slices: align each slice to a middle reference with a
similarity/affine transform.
```python
warp = np.eye(2, 3, dtype=np.float32)
_, warp = cv2.findTransformECC(ref_gray, gray, warp, cv2.MOTION_AFFINE,
                               (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5)
aligned = cv2.warpAffine(img, warp, ref.shape[1::-1], flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
```
Align consecutive pairs and chain the transforms when the stack is deep (outer slices look very
different from the reference). Tested: a slice scaled by 1.01 and shifted (2, -1.5) px was recovered
by the ECC affine call above (scale 1.010, mean abs error against the true slice 10.6 before, 1.05
after).

## 3. Sharpness map
`|Laplacian(GaussianBlur(gray))|` smoothed with a Gaussian (sigma a few pixels) per slice.

## 4. Fuse
- **Max-sharpness selection**: index = argmax over slices per pixel; fast but produces halos and
  seams (two-slice test with the left half sharp in one and the right half in the other: the
  smoothed Laplacian map picked the right slice for 91% and 72% of the pixels away from the
  boundary, and the fused result had mean error 1.14 grey levels against 6.47 for the reference
  slice alone). Smooth the index map or use soft weights (softmax of sharpness with a temperature).
- **Laplacian pyramid fusion**: at each pyramid level take the coefficient with the highest
  absolute value (or local energy) across slices; average the top Gaussian level. Fewer halos.
- `enfuse --exposure-weight=0 --saturation-weight=0 --contrast-weight=1 --hard-mask --contrast-window-size=9 *.tif`
  (with `align_image_stack -m -a al_ *.tif` first) is the classic open-source tool (gated: unconfirmed, source is paywalled or blocked); enfuse and
  align_image_stack are not installed here, so these flags were not run.

## 5. Depth map bonus
argmax slice index x focus step gives a coarse depth map (depth from focus); clean with a median
filter and a confidence threshold on peak sharpness.

## Gotchas
Moving subjects (insects, plants in wind) ghost; overlapping edges at depth discontinuities form
halos.

## Verify
Inspect high-contrast depth edges at 100 percent for halos; compare sharpness across the frame against
each source slice.
