---
id: computing-software.computer-graphics-engineering.shader-programming.cosine-colour-palettes
name: cosine-colour-palettes
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, procedural-patterns, cosine-palette, colour-palette, gradient, procedural-colour, iq-palette]
level: intro
status: draft
description: "Generate smooth procedural colour gradients in shaders with Inigo Quilez cosine palettes (a + b*cos(2pi(c*t+d))), choosing parameters and avoiding banding."
sources: ["https://iquilezles.org/articles/palettes/", "https://thebookofshaders.com/06/", "http://dev.thi.ng/gradients/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cosine colour palettes

## 1. Formula
```glsl
vec3 palette(float t, vec3 a, vec3 b, vec3 c, vec3 d) {
    return a + b * cos(6.2831853 * (c * t + d));
}
```
- `a` = offset (mid colour), `b` = amplitude (contrast), `c` = frequency per channel,
  `d` = phase per channel. All vec3, typically in 0..1.
- Four vec3 constants describe a whole gradient: cheaper than a texture lookup and continuous.

## 2. Known-good presets (Quilez)
```glsl
palette(t, vec3(.5), vec3(.5), vec3(1.0), vec3(0.00, 0.33, 0.67));   // rainbow
palette(t, vec3(.5), vec3(.5), vec3(1.0), vec3(0.00, 0.10, 0.20));   // warm
palette(t, vec3(.5), vec3(.5), vec3(1.0, 1.0, 0.5), vec3(0.80, 0.90, 0.30));
palette(t, vec3(.5), vec3(.5), vec3(2.0, 1.0, 0.0), vec3(0.50, 0.20, 0.25));
```
Use an interactive editor (thi.ng gradients) to tune, then paste the numbers.

## 3. Use
- Drive `t` with noise, distance fields, iteration counts (fractals), or time.
- Keep `a + |b| <= 1` and `a - |b| >= 0` per channel to avoid clipping.
- The formula outputs display-referred colour; if your pipeline is linear, convert
  (`pow(col, vec3(2.2))` or a proper sRGB decode) before lighting.

## Gotchas
- Banding in 8-bit targets on slow gradients: add blue-noise dither of +-0.5/255 before output.
- `c` values that aren't integers make `t=0` and `t=1` colours differ (palette doesn't loop);
  use integer `c` for cyclic animation.

## Verify
- [ ] No clipped channels across t in [0,1] (plot each channel).
- [ ] Looping animation has no jump at wrap.
