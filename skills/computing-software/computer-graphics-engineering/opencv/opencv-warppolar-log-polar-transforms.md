---
id: computing-software.computer-graphics-engineering.opencv.opencv-warppolar-log-polar-transforms
name: opencv-warppolar-log-polar-transforms
category: computing-software
field: computer-graphics-engineering
product: opencv
tags: [computer-graphics-engineering, opencv, cv-geometric-transforms, warppolar, log-polar, polar-unwrap, imgproc]
level: practitioner
status: docs-checked
description: "Unwrap circular content with OpenCV warpPolar: linear vs semilog (log-polar) modes, centre/maxRadius/dsize choices, inverse mapping, and use for gauges and rings."
sources: ["https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html", "https://en.wikipedia.org/wiki/Log-polar_coordinates"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# warpPolar and log-polar transforms

`cv2.warpPolar(src, dsize, center, maxRadius, flags)` produces the same result as the deprecated `linearPolar` and
`logPolar` (the docs mark both Deprecated and point to warpPolar).

```python
h, w = img.shape[:2]
c = (w / 2, h / 2); R = min(c)
polar = cv2.warpPolar(img, (0, 0), c, R, cv2.INTER_LINEAR + cv2.WARP_POLAR_LINEAR)
```
- Linear is the default mode; add `WARP_POLAR_LOG` to flags for the semilog mapping.
- In the destination, radius runs along x (`dsize.width / maxRadius` per unit) and angle along y
  (`dsize.height / 2*pi` per radian).
- `dsize`: if both values are <= 0 (default), the output has about the area of the bounding circle:
  width = round(maxRadius), height = round(maxRadius * pi). If only height <= 0, height = round(width * pi).
  If both are > 0 the circle is scaled to that size. Set it explicitly for predictable resolution.

## Log-polar
`flags = cv2.INTER_LINEAR + cv2.WARP_POLAR_LOG`. The radial coordinate becomes proportional to the natural log of the
distance from the centre, which emulates foveal vision (high acuity on the line of sight, lower in the periphery).
Because radius is logarithmic, scaling about the centre becomes a shift along x, and rotation a shift along y.

## Inverse
Add `WARP_INVERSE_MAP` to flags and pass the original image size as `dsize`:
`cv2.warpPolar(polar, (w, h), c, R, cv2.INTER_LINEAR + cv2.WARP_POLAR_LINEAR + cv2.WARP_INVERSE_MAP)`.
For the log mode add `WARP_POLAR_LOG` as well.

## Applications
- Unwrapping dials, rings and caps so circular features become straight lines.
- The centre must be accurate; a few pixels off turns circles into sinusoids in the unwrapped image.

## Verify
Unwrap a synthetic image of concentric circles: each must become a vertical straight line.

## Checked
2026-11-01. Confirmed in the OpenCV imgproc geometric transformations page (warpPolar, WarpPolarMode, linearPolar and
logPolar deprecation, dsize rules, WARP_INVERSE_MAP) and the formula for log-polar mapping. Removed unconfirmed: the
rotate-to-horizontal tip, phaseCorrelate Fourier-Mellin recipe, HoughCircles/fitEllipse, BORDER_WRAP padding, iris and
tyre applications, and the ellipse rectification note.
Method: documentation only; no commands were run.
