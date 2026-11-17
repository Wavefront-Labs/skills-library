---
id: computing-software.computer-graphics-engineering.opencv.opencv-unsharp-mask-sharpening
name: opencv-unsharp-mask-sharpening
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-filtering, unsharp-mask, sharpening, gaussianblur, addweighted, imgproc]
level: practitioner
status: docs-checked
description: "Sharpen images in OpenCV with unsharp masking: Gaussian-difference formula, amount/radius/threshold controls and luminance-only sharpening."
sources: ["https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html", "https://docs.opencv.org/4.x/d2/de8/group__core__array.html", "https://en.wikipedia.org/wiki/Unsharp_masking"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unsharp masking in OpenCV

`sharp = img + amount * (img - blur(img, sigma))`, optionally only where the detail exceeds a
threshold. OpenCV has no single call; compose it.

```python
def unsharp(img, sigma=1.5, amount=1.0, threshold=0):
    f = img.astype(np.float32)
    blur = cv2.GaussianBlur(f, (0, 0), sigma)       # zero ksize: computed from sigma
    detail = f - blur
    if threshold > 0:
        detail[np.abs(detail) < threshold] = 0       # leave low-contrast areas alone
    out = f + amount * detail
    return np.clip(out, 0, 255).astype(np.uint8)
```
One-liner variant: `cv2.addWeighted(img, 1 + amount, blur, -amount, 0)`; `addWeighted` computes
`saturate(src1*alpha + src2*beta + gamma)`, so the result saturates once.

## Controls (per the general description of digital unsharp masking)
- **radius (sigma)**: a smaller radius enhances smaller-scale detail; larger values can cause halos
  at edges. Radius and amount interact.
- **amount**: strength of the effect. The Wikipedia article gives a typical starting range of
  radius 0.5 to 2 pixels and amount 50 to 150 percent, and notes meanings differ between tools.
- **threshold**: minimal brightness change that gets sharpened; it stops smooth areas becoming
  speckled. Higher values exclude lower-contrast areas.

## Sharpen luminance only
```python
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
lab[..., 0] = unsharp(lab[..., 0])
img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
```

## Verify
- Inspect a step edge for overshoot or halos at your chosen amount and radius.
- Flat regions should barely change when a threshold is set.

## Checked
2026-11-01. Confirmed: the unsharp formula and the amount, radius, threshold controls with their
effects (Wikipedia, Unsharp masking); GaussianBlur zero ksize computed from sigma and addWeighted's
saturate formula (OpenCV 4.x imgproc filter and core array references). Removed: sigma, amount and
threshold ranges not in a page, the 3x3 Laplacian kernel remarks, the pipeline-order advice and the
overshoot percentage.
Method: documentation only; no commands were run.
