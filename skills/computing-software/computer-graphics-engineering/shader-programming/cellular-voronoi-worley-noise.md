---
id: computing-software.computer-graphics-engineering.shader-programming.cellular-voronoi-worley-noise
name: cellular-voronoi-worley-noise
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, procedural-patterns, voronoi, worley-noise, cellular-noise, f2-f1, procedural-textures]
level: practitioner
status: draft
description: "Implement cellular (Worley/Voronoi) noise in shaders: 3x3 neighbour search, F1/F2 distances, cell IDs, edge distance, animation and tiling."
sources: ["https://thebookofshaders.com/12/", "https://iquilezles.org/articles/voronoilines/", "https://www.rhythmiccanvas.com/research/papers/worley.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cellular / Voronoi noise

## 1. Basic F1/F2 (2D)
```glsl
vec2 hash2(vec2 p) {   // cheap hash, replace with a better one for quality
  p = vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)));
  return fract(sin(p) * 43758.5453);
}
vec3 voronoi(vec2 x) {           // returns F1, F2, cell id hash
  vec2 n = floor(x), f = fract(x);
  float f1 = 8.0, f2 = 8.0; float id = 0.0;
  for (int j = -1; j <= 1; j++)
  for (int i = -1; i <= 1; i++) {
    vec2 g = vec2(i, j);
    vec2 o = hash2(n + g);                 // feature point in the neighbour cell
    // o = 0.5 + 0.5 * sin(uTime + 6.2831 * o);   // animate
    vec2 r = g + o - f;
    float d = dot(r, r);
    if (d < f1) { f2 = f1; f1 = d; id = dot(n + g, vec2(7.0, 113.0)); }
    else if (d < f2) f2 = d;
  }
  return vec3(sqrt(f1), sqrt(f2), id);
}
```
3D version loops 3x3x3 (27 cells). Use F1 for cells/blobs, F2 - F1 for cracks/edges, id for
per-cell colour.

## 2. Exact border distance
F2 - F1 is not a true distance to the edge; for uniform-width lines use Quilez's two-pass method
(find nearest point, then distance to bisector planes of neighbours in a 5x5 search).

## 3. Metrics and variants
Manhattan (`abs(r.x)+abs(r.y)`) gives diamond cells; Chebyshev (`max`) gives squares.
fBm over Worley adds detail (clouds, stone). Smooth Voronoi blends distances with an exponential
for soft cells.

## 4. Tiling
Wrap cell coordinates with `mod(n + g, period)` before hashing so the pattern tiles.

## Gotchas
- `sin`-based hashes show artefacts at large coordinates and differ across GPUs; use an integer
  hash (PCG) when you need stability.
- Search range 3x3 is enough only if feature points stay inside their cell (jitter <= 1).

## Verify
- [ ] Visualise F1, F2-F1 and id; no discontinuities at cell boundaries.
