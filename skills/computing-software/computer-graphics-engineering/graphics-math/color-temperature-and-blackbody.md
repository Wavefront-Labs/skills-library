---
id: computing-software.computer-graphics-engineering.graphics-math.color-temperature-and-blackbody
name: color-temperature-and-blackbody
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, colour-science, color-temperature, blackbody, cct, planckian-locus, white-balance]
level: practitioner
status: verified
description: "Convert colour temperature to RGB: Planck blackbody spectra to CIE XYZ, Kelvin-to-xy approximations, CCT from chromaticity (McCamy), Duv tint, and light colour in renderers."
sources: ["https://www.fourmilab.ch/documents/specrend/", "https://cie.co.at/publications/colorimetry-4th-edition", "https://en.wikipedia.org/wiki/Planckian_locus", "https://www.colour-science.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colour temperature and blackbody

## Blackbody spectrum
Planck: `B(lambda, T) = 2 h c^2 / lambda^5 / (exp(h c / (lambda k T)) - 1)`. Integrate against CIE
1931 colour matching functions to get XYZ, normalise (Y = 1), then convert to linear RGB of the
working space (sRGB/Rec.709 or ACEScg matrix) and normalise the max channel to 1 for a light colour.
```python
import colour
xy = colour.temperature.CCT_to_xy_CIE_D(6500)          # daylight locus (D illuminants)
xy_bb = colour.temperature.CCT_to_xy_Kang2002(3200)    # Planckian approximation, 1667..25000 K
XYZ = colour.xy_to_XYZ(xy_bb)
rgb = colour.XYZ_to_RGB(XYZ, colour.RGB_COLOURSPACES["sRGB"], apply_cctf_encoding=False)
rgb /= rgb.max()
```
- Daylight (D series) and blackbody loci differ above about 4000 K: D65 is not a 6500 K blackbody
  (it lies slightly above the Planckian locus, toward green).
- Many quick "Kelvin to RGB" curve fits from the web output sRGB-encoded values; in a linear renderer,
  decode them or use the XYZ route.

## CCT from chromaticity
McCamy's approximation: `n = (x - 0.3320) / (0.1858 - y)`,
`CCT = 449 n^3 + 3525 n^2 + 6823.3 n + 5520.33` (accurate near the locus; check McCamy 1992 for the stated range; computed here: D65 gives 6505 K, Illuminant A (0.4476, 0.4074) gives 2856 K). Robertson's
or Ohno's methods are more accurate. **Duv** (distance from the locus in CIE 1960 uv) quantifies green
or magenta tint; CCT alone does not specify a colour.

## In renderers and cameras
- Most engines and DCC tools offer a light temperature (Kelvin) control; check whether yours uses a Planckian or daylight approximation.
- White balance adapts the scene white to the display white: use a chromatic adaptation transform
  (Bradford/CAT16) from the source white xy to D65, not per-channel scaling in display RGB.

## Verify
Computed here: integrating Planck at 6504 K against the CIE 1931 2-degree CMFs gives xy (0.3135, 0.3236) vs D65 (0.3127, 0.3290), Duv about +0.003 (D65 above the locus); 2856 K gives (0.4475, 0.4074), matching Illuminant A (0.4476, 0.4074).
