---
id: computing-software.computer-graphics-engineering.shader-programming.pixelation-dithering-retro-effects
name: pixelation-dithering-retro-effects
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, post-processing-shaders, pixelation, ordered-dithering, bayer-matrix, palette-quantization, retro-effects, crt-shader]
level: practitioner
status: draft
description: "Create pixelation, ordered (Bayer) dithering, palette quantisation and CRT-style retro post effects with stable results under camera motion."
sources: ["https://en.wikipedia.org/wiki/Ordered_dithering", "https://www.shadertoy.com/view/4tj3Dy", "https://github.com/libretro/glsl-shaders"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pixelation, dithering and retro effects

## 1. Pixelation
Best: render the scene to a low-res target (e.g. 320x180) with point filtering and upscale by an
integer factor. Post-process alternative:
```glsl
vec2 px = vec2(320.0, 180.0);
vec2 uvq = (floor(uv * px) + 0.5) / px;
vec3 c = texture(scene, uvq).rgb;          // sample nearest; use texelFetch on a low-res target
```
Post-process pixelation of a full-res render still shows sub-pixel aliasing; low-res rendering is
cleaner.

## 2. Ordered dithering (Bayer)
```glsl
const float bayer4[16] = float[](0., 8., 2.,10., 12., 4.,14., 6., 3.,11., 1., 9., 15., 7.,13., 5.);
float threshold(ivec2 p) { return (bayer4[(p.y & 3) * 4 + (p.x & 3)] + 0.5) / 16.0; }

vec3 quantize(vec3 c, float levels, ivec2 p) {
    float t = threshold(p) - 0.5;
    return floor(c * (levels - 1.0) + 0.5 + t) / (levels - 1.0);
}
```
- Index the matrix by the **low-res pixel coordinate** so the pattern aligns with big pixels.
- Bayer 8x8 or a blue-noise texture gives finer gradients; blue noise looks less structured.
- Dither in the colour space you quantise in (sRGB for display palettes).

## 3. Palette quantisation
- Fixed palette (e.g. PICO-8, Game Boy 4 greens): find the nearest palette colour after adding the
  dither offset; measure distance in a perceptual space (OKLab) for better matches.
- Fast path: a 3D LUT (32^3) mapping RGB -> palette index, baked offline.

## 4. Stability under camera motion
- Snap the camera position to the low-res pixel grid (in view space) and shift the final upscale by
  the sub-pixel remainder: removes shimmer when panning (the "pixel-perfect" camera trick).
- World-space dithering (screen-door patterns anchored to objects) swims less than screen-space.

## 5. CRT
Scanlines (`sin(uv.y * h * PI)`), shadow mask/aperture grille, barrel distortion, slight bloom.
libretro `crt-royale`/`crt-geom` are reference implementations.

## Gotchas
- Applying dithering before tonemapping makes it vanish or amplify; do it last.
- Non-integer upscale factors make pixels uneven widths; letterbox to integer scale.

## Verify
- [ ] No shimmering of the dither pattern while the camera pans slowly.
- [ ] Palette output uses only allowed colours (histogram check).
