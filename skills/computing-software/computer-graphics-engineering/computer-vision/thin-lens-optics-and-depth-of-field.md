---
id: computing-software.computer-graphics-engineering.computer-vision.thin-lens-optics-and-depth-of-field
name: thin-lens-optics-and-depth-of-field
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, image-formation, thin-lens-optics, depth-of-field, circle-of-confusion, hyperfocal-distance, defocus]
level: practitioner
status: verified
description: "Apply thin-lens optics in vision: focus distance, circle of confusion, depth of field and hyperfocal formulas, f-number vs blur, and depth from defocus/focus measurements."
sources: ["https://szeliski.org/Book/", "https://en.wikipedia.org/wiki/Depth_of_field", "https://en.wikipedia.org/wiki/Circle_of_confusion"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thin lens optics, focus and depth of field

## Thin lens equation
`1/f = 1/z_o + 1/z_i` (object distance z_o, image distance z_i). Pinhole intrinsics `fx` (pixels)
relate to the physical lens by `fx = z_i / pixel_pitch`, which is about `f / pixel_pitch` when
focused far away. Refocusing changes z_i, so **focal length in pixels changes with focus** (focusing at 1 m with f = 8 mm gives z_i = 8.06 mm, 0.8%
larger)
(focus breathing): calibrate at the focus setting you will use and lock focus.

## Circle of confusion
For a lens focused at distance s, a point at distance d gives a blur disc of diameter
`c = A * |d - s| / d * f / (s - f)`, where aperture diameter `A = f / N` (N = f-number).
In pixels: `c / pixel_pitch`.

## Depth of field
With acceptable blur c (commonly 1 to 2 pixels for CV):
- Hyperfocal distance `H = f^2 / (N c) + f`.
- Near limit `D_n = s (H - f) / (H + s - 2f)`, far limit `D_f = s (H - f) / (H - s)` (infinite
  if s >= H).
Example: f = 8 mm, N = 4, c = 2 x 3.45 um: H is about 2.3 m (computed 2.327 m), so focusing at H
gives sharp images from about 1.2 m (computed 1.163 m) to infinity. The formulas were checked
against the circle-of-confusion expression: blur at the near limit, at infinity (focus at H) and at
the far limit for s = 1.5 m (D_f = 4.21 m) all came out at exactly 2.00 px.

## Trade-offs
- Stopping down (larger N) increases DOF but needs more light and hits diffraction: Airy disc
  diameter about `2.44 * lambda * N` (green light at 550 nm, N = 8 gives 10.7 um, i.e. 3.1 px on a 3.45 um
  sensor, computed).
- Wider lenses and smaller sensors have more DOF at the same N.

## Using defocus as a cue
- Depth from focus: sweep focus, pick per-pixel sharpest slice (Laplacian variance); this is the
  basis of focus stacking.
- Depth from defocus: compare blur between two apertures/focus settings; ambiguity in front of vs
  behind the focal plane.

## Verify
Photograph a slanted ruler or Siemens star at multiple distances; measure the blur width and
compare with the predicted circle of confusion.
