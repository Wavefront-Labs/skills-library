---
id: computing-software.computer-graphics-engineering.graphics-math.perceptual-colour-spaces-oklab-and-luminance
name: perceptual-colour-spaces-oklab-and-luminance
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, colour-science, oklab, oklch, luminance, relative-luminance, cielab, delta-e, gradient-interpolation, perceptual-uniformity]
level: practitioner
status: verified
description: "Use perceptual colour maths in graphics code: relative luminance weights, OKLab/OKLCH conversions for gradients and palette edits, colour difference metrics."
sources: ["https://bottosson.github.io/posts/oklab/", "https://www.w3.org/TR/css-color-4/#ok-lab", "https://www.w3.org/TR/WCAG21/#dfn-relative-luminance", "Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 8.1.3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Perceptual colour spaces: OKLab and luminance

**Goal:** colour operations that look right to humans — gradients, palette generation,
contrast checks, colour-based thresholds — while lighting stays physically linear.

## 1. Linear RGB vs perceptual spaces
- **Lighting, blending, filtering, mip generation**: linear RGB (physics is additive in
  linear light).
- **Gradients, UI palettes, hue shifts, "lighten by 10%", colour distance**: perceptual space
  (OKLab/OKLCH, CIELAB) — equal steps look equal.

## 2. Relative luminance
For **linear** Rec.709/sRGB primaries:
`Y = 0.2126 R + 0.7152 G + 0.0722 B` (computed from the Rec.709 primaries and D65: 0.21264, 0.71517, 0.07219)
(Not 0.299/0.587/0.114 — those are Rec.601 luma weights on gamma-encoded values.) Use Y for
exposure metering, bloom thresholds, luminance-preserving desaturation, contrast ratios
(WCAG: `(L1 + 0.05) / (L2 + 0.05)` with Y of the decoded sRGB colours).

## 3. OKLab (Björn Ottosson, 2020)
```glsl
vec3 linearSrgbToOklab(vec3 c) {
    float l = 0.4122214708*c.r + 0.5363325363*c.g + 0.0514459929*c.b;
    float m = 0.2119034982*c.r + 0.6806995451*c.g + 0.1073969566*c.b;
    float s = 0.0883024619*c.r + 0.2817188376*c.g + 0.6299787005*c.b;
    l = pow(l, 1.0/3.0); m = pow(m, 1.0/3.0); s = pow(s, 1.0/3.0);   // cbrt; handle negatives with sign()
    return vec3(0.2104542553*l + 0.7936177850*m - 0.0040720468*s,
                1.9779984951*l - 2.4285922050*m + 0.4505937099*s,
                0.0259040371*l + 0.7827717662*m - 0.8086757660*s);
}
```
Inverse: apply the inverse matrices and cube. **OKLCH** = polar form (L, C = |ab|, h = atan2(b,a))
for hue rotation and chroma control. CSS Color 4 supports `oklch()` natively.

## 4. Uses
- Gradients: interpolate in OKLab → no muddy grey midpoint between complementary colours
  (as happens in sRGB) and no hue drift (as in HSV).
- Palette generation: fix L for consistent perceived brightness, vary h.
- Colour difference: Euclidean distance in OKLab is a decent ΔE; for colour-critical work use
  CIEDE2000 in CIELAB.

## Gotchas
- Input must be **linear** sRGB (decode the sRGB transfer first).
- Out-of-gamut results when increasing chroma — clamp chroma in OKLCH or gamut-map before
  converting back.
- HSV/HSL "lightness" is not perceptual: yellow and blue at the same V look very different.

## Verify
- [ ] Round-trip sRGB → OKLab → sRGB within 1e-5.
- [ ] Reference values match Ottosson's published test colours. Computed here: linear white gives L=1.000, a,b about 0 (1e-8); linear red gives (0.628, 0.225, 0.126), matching colour-science `XYZ_to_Oklab`.
- [ ] Luminance code uses linear-light inputs with Rec.709 weights.
