---
id: computing-software.computer-graphics-engineering.graphics-math.numerical-robustness-in-graphics-math
name: numerical-robustness-in-graphics-math
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [graphics-math, floating-point, numerical-precision, z-fighting, epsilon, gimbal-lock, quaternion-drift, matrix-orthonormalization, depth-precision, catastrophic-cancellation, double-precision, large-world-coordinates]
level: advanced
status: draft
description: "Floating-point failure modes specific to real-time graphics: z-fighting, depth precision, quaternion/matrix drift, gimbal lock, large-world coordinate jitter, and the fixes."
sources: ["https://developer.nvidia.com/content/depth-precision-visualized", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Numerical robustness in graphics math

**Goal:** recognise the handful of floating-point failure modes that are specific
to real-time graphics (not generic numerics) before they show up as visual
artefacts, and apply the standard fix rather than a local hack.

## Depth precision and z-fighting
- Standard perspective projection maps depth **nonlinearly** into
  `[0,1]`/`[-1,1]` — precision is dense near the near plane, extremely sparse near
  the far plane. Two surfaces close in world space but far from the camera can map
  to the *same* depth-buffer value → **z-fighting** (flickering overlap).
- Fixes, in order of effectiveness: **reverse-Z** (map far→0, near→1; matches
  float precision's higher density near 0, a near-free win with a 32-bit float
  depth buffer), increasing near-plane distance (the single biggest lever — doubling
  the near plane roughly halves precision loss, quadrupling the far/near ratio
  roughly halves it too), logarithmic depth (for extreme far/near ratios, at the
  cost of needing per-vertex depth adjustment and breaking some hardware depth
  optimisations).
- Coplanar geometry intentionally overlapping (decals on a surface) needs an
  explicit depth bias / polygon offset, not reliance on z-buffer precision to
  separate them.

## Quaternion and matrix drift
- Repeatedly multiplying rotation matrices or quaternions accumulates floating-
  point error; after enough frames a "rotation" matrix stops being orthonormal
  (shears/scales creep in) and a quaternion stops being unit length.
- Fix: **re-normalize quaternions every frame** (cheap, `q / length(q)`) and
  **re-orthonormalize rotation matrices periodically** (Gram-Schmidt on the basis
  vectors) if you must accumulate matrices directly — better: store orientation as
  a quaternion and rebuild the matrix from it each frame rather than accumulating
  the matrix.
- **Gimbal lock**: Euler angles lose a degree of freedom when two of the three
  rotation axes align (e.g. pitch at ±90°) — inherent to the Euler representation,
  not a bug to "fix" within Euler angles. Use quaternions for interpolation/
  accumulation; keep Euler only as a human-readable edit representation, converted
  to/from quaternion at the boundary.

## Large-world coordinate jitter
- float32 has ~7 decimal digits of precision; at world coordinates in the tens of
  thousands, the gap between representable values exceeds sub-millimetre scale —
  visible as vertex "swimming"/jitter, especially under camera movement.
- Fixes: **camera-relative rendering** (translate geometry so the camera is near
  the origin before the GPU-side transform — do the subtraction in double/CPU
  precision, upload camera-relative floats), **origin rebasing** (periodically
  shift the whole world's origin to stay near the active area — open-world
  engines do this), or double precision on CPU for world-space math with a
  float32 cast only at the final camera-relative step.

## Catastrophic cancellation and near-zero epsilons
- Subtracting two nearly-equal large floats (common in ray-plane/ray-triangle
  intersection near grazing angles) amplifies relative error — reformulate to
  avoid the subtraction where possible (e.g. solve for the smaller quantity
  directly) rather than subtracting then normalising.
- Epsilon comparisons (`abs(a-b) < EPS`) need a **scale-relative** epsilon
  (`EPS * max(abs(a), abs(b))`) for values that aren't near 0 — a fixed small
  epsilon that works near the origin silently stops working at larger magnitudes.

## Verify
- [ ] Depth buffer configuration checked (reverse-Z + float32 depth is the modern
      default) rather than assumed from an old tutorial's default.
- [ ] Orientation state stored as quaternion (or re-orthonormalized matrix), not
      accumulated raw matrix multiplication, for anything rotated over many frames.
- [ ] Large-coordinate scenes tested at the actual far-from-origin distances used
      in production, not just near the origin where jitter doesn't show.
- [ ] Epsilon comparisons checked for scale-relativity where values aren't bounded
      near zero.
