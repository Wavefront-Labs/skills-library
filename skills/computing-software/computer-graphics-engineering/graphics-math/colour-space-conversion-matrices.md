---
id: computing-software.computer-graphics-engineering.graphics-math.colour-space-conversion-matrices
name: colour-space-conversion-matrices
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, colour-science, color-science, rec2020, acescg, gamut-mapping, rec709, display-p3, rgb-to-xyz, primaries, opencolorio]
level: advanced
status: verified
description: "Convert between RGB colour spaces correctly: deriving RGB-to-XYZ matrices from primaries and white point, Rec.709/P3/Rec.2020/ACEScg conversions in linear light."
sources: ["Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 8.1", "https://pbr-book.org/4ed/Radiometry,_Spectra,_and_Color/Color", "https://www.itu.int/rec/R-REC-BT.2020", "https://docs.acescentral.com/", "https://opencolorio.readthedocs.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colour space conversion matrices

**Goal:** colours that stay the same colour when moving between sRGB textures, a wide-gamut
working space, and HDR/wide-gamut displays (see RTR4 and PBR4 colour chapters).

## 1. An RGB space = primaries + white point + transfer function
| space | primaries | white | typical use |
|---|---|---|---|
| sRGB / Rec.709 | 709 | D65 | textures, SDR displays |
| Display P3 | P3 | D65 | Apple displays, web wide gamut |
| Rec.2020 | 2020 | D65 | HDR10 output container |
| ACEScg (AP1) | AP1 | ACES white (close to D60; confirm in the ACES spec) | VFX rendering working space |
| ACES2065-1 (AP0) | AP0 | ACES white (close to D60) | archival interchange |
Matrices act on **linear** values only: decode the transfer function (sRGB EOTF, PQ) first,
convert, re-encode.

## 2. Derive RGB → XYZ from primaries
Given chromaticities (x, y) of R, G, B and white W:
```python
def rgb_to_xyz(prims, white):
    P = np.array([[x / y, 1.0, (1 - x - y) / y] for x, y in prims]).T   # columns: XYZ of each primary (Y=1)
    W = np.array([white[0] / white[1], 1.0, (1 - white[0] - white[1]) / white[1]])
    S = np.linalg.solve(P, W)                  # scale primaries so R=G=B=1 maps to white
    return P * S
M709  = rgb_to_xyz([(0.64, 0.33), (0.30, 0.60), (0.15, 0.06)], (0.3127, 0.3290))
M2020 = rgb_to_xyz([(0.708, 0.292), (0.170, 0.797), (0.131, 0.046)], (0.3127, 0.3290))
M_709_to_2020 = np.linalg.inv(M2020) @ M709
# computed: [[0.6274, 0.3293, 0.0433], [0.0691, 0.9195, 0.0114], [0.0164, 0.0880, 0.8956]]
```
Different white points (ACEScg's D60 vs D65) need chromatic adaptation (Bradford/CAT02)
between the two XYZ conversions.

## 3. In practice
- Keep rendering in one linear working space (Rec.709/sRGB primaries for most real-time;
  ACEScg or Rec.2020 for wide-gamut pipelines) and convert textures on import.
- For VFX/film pipelines use **OpenColorIO** configs (ACES) rather than hand-rolled matrices.
- Matrices are 3x3 per pixel — fold them into the tone-mapping/output shader.

## 4. Out-of-gamut values
Converting a wide-gamut colour into a smaller gamut yields negative or >1 components.
- Clipping per channel shifts hue; better: gamut compression (ACES Reference Gamut
  Compression) or desaturate toward the luminance-preserving neutral.
- Negative values in a linear working space can be valid intermediate data — clamp only at
  output.

## Gotchas
- Applying matrices to sRGB-encoded values (non-linear) gives wrong colours, subtly.
- Row vs column vector conventions: verify by converting pure white (must stay white) and
  pure primaries.
- "Rec.2020 output" for HDR10 still usually contains Rec.709-gamut content — that's expected.

## Verify
- [ ] White (1,1,1) maps to white in every conversion (same white point).
- [ ] Round-trip A→B→A within 1e-5 for in-gamut colours.
- [ ] Matrices match published values (the 709→2020 matrix above was computed here; confirm the published figures in ITU-R BT.2087).
