---
id: computing-software.computer-graphics-engineering.graphics-math.adaptive-curve-flattening
name: adaptive-curve-flattening
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, curves-surfaces, curve-flattening, bezier-curves, adaptive-subdivision, vector-graphics, tessellation]
level: advanced
status: draft
description: "Flatten Bezier curves into line segments adaptively: tolerance-based subdivision, flatness tests, Wang's formula, parabola-based flattening and strokes."
sources: ["https://raphlinus.github.io/graphics/curves/2019/12/23/flatten-quadbez.html", "https://www.cs.cmu.edu/~fp/courses/graphics/asst5/cubicSubdiv.pdf", "https://pomax.github.io/bezierinfo/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adaptive curve flattening

Rasterisers, path renderers and CNC/plotters need polylines within a tolerance (e.g. 0.25 px or
0.01 mm) of the true curve with as few segments as possible.

## Recursive subdivision with a flatness test
```cpp
void flatten(Cubic c, float tol, std::vector<vec2>& out) {
    // flatness: max distance of control points from chord (cheap bound)
    vec2 u = 3.0f * c.p1 - 2.0f * c.p0 - c.p3, v = 3.0f * c.p2 - c.p0 - 2.0f * c.p3;
    float d = std::max(dot(u, u), dot(v, v));           // Roger Willcocks' bound: 16 * maxdist^2
    if (d <= 16.0f * tol * tol) { out.push_back(c.p3); return; }
    Cubic a, b; c.split(0.5f, a, b);                    // de Casteljau
    flatten(a, tol, out); flatten(b, tol, out);
}
```
Recursion depth cap (e.g. 16) guards against NaN/huge inputs.

## Wang's formula (segment count without recursion)
For a degree-n Bezier, uniform parameter steps with
`N = ceil( sqrt( n (n-1) / (8 tol) * max_i |P_{i+2} - 2 P_{i+1} + P_i| ) )` guarantee the tolerance.
GPU-friendly (fixed count per curve, used in Skia's GPU tessellation), but over-subdivides curves with
uneven curvature.

## Parabola-based (Levien)
For quadratics, map to a standard parabola and use an integral approximation to place points so each
segment has roughly equal error: near-optimal count with no recursion. Cubics: approximate by
quadratics first, then flatten.

## Tolerance in device space
Flatten after applying the transform (or scale tolerance by the transform's max scale); flattening
in object space then zooming shows facets.

## Strokes
Offsetting a flattened curve is not the offset of the curve: for thick strokes flatten with tolerance
divided by a factor, or offset the curve (approximate by Beziers) then flatten. Cusps and tight
curves need joins.

## Verify
Measure max distance from densely sampled true curve points to the polyline: must be at most tol;
compare segment counts across methods.
