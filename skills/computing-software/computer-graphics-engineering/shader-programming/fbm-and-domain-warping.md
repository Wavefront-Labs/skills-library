---
id: computing-software.computer-graphics-engineering.shader-programming.fbm-and-domain-warping
name: fbm-and-domain-warping
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, procedural-patterns, fbm, domain-warping, fractal-brownian-motion, octaves, lacunarity, gain, ridged-noise, procedural-terrain]
level: practitioner
status: draft
description: "Layer noise into fractal Brownian motion and domain-warped patterns for terrain, clouds, marble and fire: octaves, lacunarity, gain, rotation between octaves."
sources: ["https://thebookofshaders.com/13/", "https://iquilezles.org/articles/fbm/", "https://iquilezles.org/articles/warp/", "https://iquilezles.org/articles/morenoise/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# fBm and domain warping

**Goal:** rich natural detail (terrain, clouds, rock, smoke) from one noise function,
tunable by a few parameters and free of shimmering.

## 1. fBm
```glsl
const mat2 ROT = mat2(0.8, 0.6, -0.6, 0.8);       // rotate each octave: hides lattice alignment
float fbm(vec2 p, int octaves, float lacunarity, float gain) {
    float sum = 0.0, amp = 0.5;
    for (int i = 0; i < octaves; ++i) {
        sum += amp * noise(p);                     // noise in [-1,1]
        p = ROT * p * lacunarity;                  // frequency x2 typical
        amp *= gain;                               // amplitude x0.5 typical
    }
    return sum;
}
```
- **lacunarity** ~2.0 (frequency step), **gain** ~0.5 (amplitude step; = 2^-H where H is the
  Hurst exponent). Gain 0.5 ↔ "pink" natural look; higher gain = rougher.
- Octave count: stop when the octave's wavelength drops below a pixel (see §4).

## 2. Variants
- **Turbulence**: `sum += amp * abs(noise(p))` — billowy clouds, fire.
- **Ridged**: `n = 1.0 - abs(noise(p)); n *= n; sum += amp * n * prev;` — mountain ridges
  (weight by previous octave for erosion-like detail).
- **Terrain with derivatives** (IQ): dampen higher octaves where slope is high, for eroded
  looks, using analytic noise derivatives.

## 3. Domain warping
Feed fBm into the coordinates of another fBm:
```glsl
float pattern(vec2 p) {
    vec2 q = vec2(fbm(p + vec2(0.0, 0.0), 5, 2.0, 0.5),
                  fbm(p + vec2(5.2, 1.3), 5, 2.0, 0.5));
    vec2 r = vec2(fbm(p + 4.0 * q + vec2(1.7, 9.2), 5, 2.0, 0.5),
                  fbm(p + 4.0 * q + vec2(8.3, 2.8), 5, 2.0, 0.5));
    return fbm(p + 4.0 * r, 5, 2.0, 0.5);
}
```
Offsets decorrelate channels; the `4.0` warp strength controls swirliness. Animate by adding
time to one offset. Use `q` and `r` magnitudes to drive colour mixing for marble/gas-giant looks.
Cost: 5 fBm × 5 octaves = 25 noise calls per pixel — bake to texture if static.

## 4. Anti-aliasing procedural detail
High octaves alias (shimmer) at distance/minification. Fade octaves by screen-space
frequency:
```glsl
float w = fwidth(p.x) + fwidth(p.y);              // footprint in noise space
float fade = clamp(1.0 - w * freq * 2.0, 0.0, 1.0);   // per octave, freq = current frequency
sum += amp * noise(p) * fade;
```

## Gotchas
- Integer `octaves` loops with dynamic counts can be slow on mobile — use constants or
  specialisation.
- fBm output range isn't normalised: max ≈ sum of amplitudes; normalise for colour mapping.
- Precision: large coordinates × lacunarity^octaves overflow mediump quickly; keep highp.

## Verify
- [ ] Zooming out shows no shimmering (octave fading works).
- [ ] Parameter sweep (gain, lacunarity) produces expected rough/smooth range.
- [ ] GPU cost measured; static patterns baked if over budget.
