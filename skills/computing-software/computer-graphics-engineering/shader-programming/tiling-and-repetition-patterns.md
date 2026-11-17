---
id: computing-software.computer-graphics-engineering.shader-programming.tiling-and-repetition-patterns
name: tiling-and-repetition-patterns
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, procedural-patterns, tiling-patterns, fract-repetition, domain-repetition, grid-shader, hex-grid, book-of-shaders]
level: practitioner
status: draft
description: "Build repeating shader patterns: fract/mod domain repetition, cell IDs, brick and hex offsets, mirrored tiles, grid lines with fwidth antialiasing, and per-cell randomisation."
sources: ["https://thebookofshaders.com/09/", "https://iquilezles.org/articles/sdfrepetition/", "https://www.redblobgames.com/grids/hexagons/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tiling, repetition and grids

## 1. Basic repetition
```glsl
vec2 st = uv * 10.0;        // 10x10 tiles
vec2 id = floor(st);        // integer cell coordinate
vec2 f  = fract(st);        // 0..1 inside cell
```
Draw anything in `f` and it repeats; use `id` to vary per tile (`hash(id)`).

## 2. Offsets and mirrors
```glsl
// brick: shift every other row by half a tile
st.x += step(1.0, mod(st.y, 2.0)) * 0.5;
// mirrored tiles (seamless symmetric pattern)
vec2 m = abs(fract(st * 0.5) * 2.0 - 1.0);
// rotate each tile by a random multiple of 90 degrees
float r = floor(hash(id) * 4.0); f -= 0.5; f = r == 1. ? vec2(-f.y, f.x) : r == 2. ? -f : r == 3. ? vec2(f.y, -f.x) : f; f += 0.5;
```

## 3. Hex grid
```glsl
vec4 hexCoords(vec2 p) {                  // returns local xy and cell id
    const vec2 s = vec2(1.0, 1.7320508);
    vec4 hc = floor(vec4(p, p - vec2(0.5, 1.0)) / s.xyxy) + 0.5;
    vec4 h  = vec4(p - hc.xy * s, p - (hc.zw + 0.5) * s);
    return dot(h.xy, h.xy) < dot(h.zw, h.zw) ? vec4(h.xy, hc.xy) : vec4(h.zw, hc.zw + 0.5);
}
```

## 4. Antialiased grid lines
```glsl
vec2 g = abs(fract(st - 0.5) - 0.5) / fwidth(st);   // distance to line in pixels
float line = 1.0 - min(min(g.x, g.y), 1.0);
```
`fwidth` keeps lines one pixel wide at any zoom; for infinite ground grids fade by distance
(`line *= 1.0 - smoothstep(near, far, viewDist)`) to hide moire.

## 5. SDF repetition in 3D
`p = p - spacing * round(p / spacing);` repeats an SDF infinitely. For limited repetition clamp:
`p - spacing * clamp(round(p / spacing), -n, n)`. Neighbouring cells must be checked if the shape
extends beyond its cell or is randomised per cell.

## Gotchas
- Large `uv * scale` loses float precision far from origin: wrap time/offsets with `mod`.
- `fract` derivatives jump at cell edges; mip selection using `fract(uv)` causes a 1-pixel seam.
  Sample with `textureGrad(tex, f, dFdx(st), dFdy(st))`.
- `mod` in GLSL vs `fmod` in HLSL differ for negatives (HLSL `fmod` keeps sign); use
  `x - y * floor(x / y)`.

## Verify
- [ ] No seams at tile borders when zooming with mipmapped textures.
- [ ] Per-tile variation driven by `id` is stable across frames.
