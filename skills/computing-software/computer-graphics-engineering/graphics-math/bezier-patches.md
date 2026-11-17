---
id: computing-software.computer-graphics-engineering.graphics-math.bezier-patches
name: bezier-patches
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, curves-surfaces, bezier-patches, bicubic-patch, tensor-product-surface, tessellation, parametric-surfaces]
level: advanced
status: draft
description: "Evaluate and tessellate bicubic Bezier patches: tensor-product de Casteljau, partial derivatives and normals, degenerate corners, continuity between patches and GPU evaluation."
sources: ["https://pomax.github.io/bezierinfo/", "https://www.realtimerendering.com/", "https://www.khronos.org/opengl/wiki/Tessellation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bezier patches

## Definition
A bicubic patch has a 4x4 grid of control points P_ij:
`S(u, v) = sum_i sum_j B_i(u) B_j(v) P_ij` with cubic Bernstein `B_0 = (1-t)^3, B_1 = 3t(1-t)^2,
B_2 = 3t^2(1-t), B_3 = t^3`. It interpolates the 4 corners; boundary curves are cubic Beziers defined
by the edge rows/columns.

## Evaluation
Tensor product: evaluate 4 cubic curves along u (one per row), then one cubic along v through the
results. Or matrix form `S = U M P M^T V^T` with the Bezier basis matrix M (fast for many samples:
precompute basis values per (u, v) once).

## Normals
`n = normalize(dS/du x dS/dv)`. Derivatives: degree-2 Bezier from control point differences,
`dS/du = 3 sum_i sum_j B2_i(u) B3_j(v) (P_{i+1,j} - P_ij)`.
**Degenerate corners** (collapsed edge, e.g. the Utah teapot lid top): one derivative is zero at the
corner, the cross product is zero; evaluate the normal at a slightly offset parameter or use the
second derivative.

## Tessellation
- Uniform grid in (u, v) with N chosen from screen-space size or curvature; share edge vertex counts
  between neighbours to avoid cracks.
- GPU: tessellation shaders with a 16-control-point patch (`layout(vertices = 16)`), evaluate in the
  TES/domain shader; edge tess factors from edge control points only.

## Continuity between patches
- C0: shared boundary control points.
- G1: control points either side of the shared edge collinear with it (and consistent ratio for C1).
Bezier patch networks around extraordinary vertices cannot be G1 with plain bicubics; that is why
subdivision surfaces and Gregory patches exist.

## Verify
Render the Utah teapot (32 patches): no cracks, smooth shading, no black normals at the lid and handle
poles.
