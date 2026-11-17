---
id: computing-software.computer-graphics-engineering.graphics-math.chromatic-adaptation-and-white-point
name: chromatic-adaptation-and-white-point
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, colour-science, chromatic-adaptation, white-point, bradford-transform, white-balance, cat16]
level: sme
status: draft
description: "Apply chromatic adaptation: von Kries/Bradford/CAT16 transforms between white points (D65, D50, ACES), white balance in renderers, and colour temperature to RGB."
sources: ["http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html", "https://www.colour-science.org/", "https://docs.acescentral.com/", "https://www.color.org/specification/ICC.1-2022-05.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# White point and chromatic adaptation

## 1. Concept
The eye adapts to the illuminant so white paper looks white under tungsten and daylight. A chromatic
adaptation transform (CAT) maps XYZ under source white to the corresponding colour under destination white:
convert to a cone-like space, scale each channel by dest/source white, convert back.
```text
M_cat = Minv * diag(rho_d/rho_s, gamma_d/gamma_s, beta_d/beta_s) * M
```
Bradford M (rows): [0.8951 0.2664 -0.1614; -0.7502 1.7135 0.0367; 0.0389 -0.0685 1.0296].
CAT02/CAT16 are newer (CIECAM02/CAM16); von Kries (diagonal in LMS) and XYZ scaling are cruder.

## 2. Where it shows up in graphics
- **Colour space conversion with different white points**: sRGB/Rec.709 and Rec.2020 use D65; ACES AP0/AP1
  use a white near D60; Display P3 D65; DCI-P3 uses DCI white; ICC profile connection space is D50.
  RGB->RGB matrices between spaces with different whites must include a CAT (e.g. Bradford) - check how your
  library builds them.
```python
import colour
M = colour.matrix_RGB_to_RGB(colour.RGB_COLOURSPACES["ACEScg"], colour.RGB_COLOURSPACES["sRGB"],
                             chromatic_adaptation_transform="Bradford")
```
- **White balance in a renderer**: lights specified by colour temperature (Kelvin) are converted to RGB via
  Planckian locus chromaticity; then the camera white balance applies a CAT from the chosen white (e.g. 3200 K)
  to D65 before tone mapping. Do this in linear space, ideally in LMS.

## 3. Kelvin to chromaticity
Planckian locus approximation (Kim et al. cubic spline) gives (x, y) for 1667-25000 K; then XYZ with Y = 1,
then to linear RGB. Daylight illuminants (D-series) are off the Planckian locus for 4000-25000 K; use the CIE
daylight formula for D55/D65/D75.

## Gotchas
- Multiplying linear RGB channels by a white-balance gain works only approximately; large shifts look wrong
  (hue shifts) compared with a CAT in LMS.
- Do not adapt twice: some ICC/OCIO configs already include adaptation in their matrices.
- Use full-precision published primaries/white coordinates; truncated values produce visible tints in greys.

## Verify
- [ ] Neutral grey ramp stays neutral after converting ACEScg -> sRGB; a 3200 K light with 3200 K white balance
  renders white.
