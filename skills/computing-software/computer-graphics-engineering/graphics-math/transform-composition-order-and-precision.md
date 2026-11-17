---
id: computing-software.computer-graphics-engineering.graphics-math.transform-composition-order-and-precision
name: transform-composition-order-and-precision
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, transforms, transform-order, matrix-multiplication, row-major, column-major, floating-point-precision]
level: practitioner
status: draft
description: "Get transform order right: column vs row vector conventions, TRS order, pre- vs post-multiplication for local/world rotations, float error accumulation and re-orthonormalisation."
sources: ["https://www.realtimerendering.com/", "https://fgiesen.wordpress.com/2012/02/12/row-major-vs-column-major-row-vectors-vs-column-vectors/", "https://glm.g-truc.net/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transform composition order and precision

## Two independent choices
- **Vector convention**: column vectors (`v' = M v`, OpenGL/GLM/math texts) vs row vectors
  (`v' = v M`, DirectXMath, classic D3D). Row convention matrices are the transpose; composition
  order reverses.
- **Storage order**: column-major vs row-major memory layout. Independent of the convention; mixing
  them up transposes the matrix when uploading (fix with `row_major`/`column_major` in HLSL/GLSL or
  transpose flag).

## TRS
Column vectors: `M = T * R * S` applies scale, then rotation, then translation to a vertex.
Rotating after translating (`R * T`) orbits the object around the origin.

## Local vs world rotations
- `M = M * R_delta`: rotate about the object's **local** axes (post-multiply).
- `M = R_delta * M`: rotate about **world** axes (pre-multiply), including orbiting around world origin.
- Rotate about a pivot p: `T(p) * R * T(-p)`.
Same with quaternions: `q = q * dq` (local), `q = dq * q` (world), for Hamilton convention with
column-vector rotation `v' = q v q*`.

## Precision
- Accumulating incremental rotations (`M = M * R_delta` each frame) drifts away from orthonormal:
  scale and shear creep in. Store orientation as a quaternion and normalise each update, or
  re-orthonormalise the matrix (Gram-Schmidt) periodically.
- Compose in the order that keeps magnitudes small: subtract the camera position (camera-relative)
  before multiplying by projection, instead of multiplying huge world coordinates by the full MVP.
- Precompute `ViewProj` in double on the CPU for large worlds, or keep model-view in float relative to
  the camera.

## Verify
Write a test that transforms a known point through each composition and compares to hand-computed
results; assert `|R^T R - I| < 1e-5` over long simulated sessions.
