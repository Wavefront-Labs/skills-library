---
id: computing-software.computer-graphics-engineering.shader-programming.truchet-tiles
name: truchet-tiles
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, procedural-patterns, truchet, tiling-patterns, procedural-art, pattern-variation, sdf-2d]
level: practitioner
status: draft
description: "Render Truchet tile patterns in shaders: random per-cell orientation of arcs or diagonals, multiscale Truchet, antialiasing with SDFs and animating flow along connected paths."
sources: ["https://thebookofshaders.com/09/", "https://en.wikipedia.org/wiki/Truchet_tiles", "https://www.shadertoy.com/view/4t3BW4"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Truchet tiles

A Truchet pattern is a grid where each cell holds the same motif in a random orientation; the
motifs connect across cell edges into continuous paths.

## 1. Quarter-circle (Smith) tiles
```glsl
float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }

float truchet(vec2 uv, float scale, float width) {
    vec2 st = uv * scale;
    vec2 id = floor(st);
    vec2 f  = fract(st) - 0.5;
    if (hash(id) < 0.5) f.x = -f.x;               // flip orientation per cell
    // distance to the two quarter-arcs centred on opposite corners
    float d = min(abs(length(f - 0.5) - 0.5), abs(length(f + 0.5) - 0.5));
    float aa = fwidth(d);
    return 1.0 - smoothstep(width - aa, width + aa, d);
}
```
Diagonal variant: `d = abs(f.x + f.y)` or `abs(f.x - f.y)` per cell (10 PRINT maze).

## 2. Flow along paths
Compute the angle around the arc centre (`atan` of `f - corner`) and add `time` to animate dashes;
flip direction on mirrored cells (and per checkerboard parity) so the flow stays continuous:
```glsl
float checker = mod(id.x + id.y, 2.0) * 2.0 - 1.0;
```

## 3. Multiscale Truchet
Recursively subdivide some cells (hash decides) into 2x2 smaller tiles with inverted colours;
the motif widths are chosen so paths still meet at edges (Carlson's multiscale Truchet).

## 4. Variations
- Hex Truchet: three arcs per hex cell connecting edge midpoints, rotated by 0/60/120 degrees.
- 3D Truchet: torus segments in voxel cells, rendered with sphere tracing.

## Gotchas
- Without `fwidth`-based edges the arcs alias badly when the pattern is minified.
- Hash quality matters: `sin`-hash shows repeating structure at large ids; use an integer hash.

## Verify
- [ ] Paths are continuous across every cell edge.
- [ ] Animated flow does not reverse at cell boundaries.
