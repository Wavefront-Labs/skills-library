---
id: computing-software.computer-graphics-engineering.graphics-math.infinite-far-plane-reversed-z-projection
name: infinite-far-plane-reversed-z-projection
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, projection, infinite-far-plane, reversed-z, depth-precision, perspective-projection, linearize-depth, linear-depth]
level: sme
status: verified
description: "Use an infinite far plane with reversed-Z: matrix derivation for [0,1] depth, float depth setup per API, linearising depth, and culling/clip implications."
sources: ["https://developer.nvidia.com/content/depth-precision-visualized", "https://www.terathon.com/gdc07_lengyel.pdf", "https://iolite-engine.com/blog_posts/reverse_z_cheatsheet", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Infinite far plane projection

## 1. Matrix (reversed-Z, depth 1 at near, 0 at infinity; right-handed, looks down -Z)
```text
f = 1 / tan(fovY/2)
| f/aspect  0   0   0 |
| 0         f   0   0 |
| 0         0   0   n |
| 0         0  -1   0 |
```
clip.z = n, clip.w = -z_view, so depth = n / -z_view: 1 at the near plane, approaching 0 at infinity.
Non-reversed infinite (GL-style [-1,1]) has third row `0 0 -1 -2n`; prefer reversed.

## 2. Setup
- Depth format D32_SFLOAT (float) - reversed-Z only pays off with float depth.
- Clear depth to 0, compare GREATER (or GREATER_EQUAL).
- OpenGL: `glClipControl(GL_LOWER_LEFT, GL_ZERO_TO_ONE)` (GL 4.5 / ARB_clip_control) or the [0,1] mapping is lost.
- Vulkan/D3D already use [0,1].
- Sky/background: draw at depth 0 (or rely on clear) with GREATER_EQUAL.

## 3. Linearise depth
`z_view_distance = n / depth` (depth from the buffer). With a finite reversed far plane (third row
`0 0 n/(f-n) n*f/(f-n)`) it is `n * f / (depth * (f - n) + n)`. Unit-test against your exact matrix.

## 4. Why infinite
- No far-plane clipping of distant terrain/sky; no need to tune far.
- With reversed float depth, precision is near-uniform in log space, so z-fighting at distance is negligible.
- Lengyel's "Projection Matrix Tricks" describes a small-epsilon infinite projection for robustness at the far plane; take the exact matrix from the paper rather than from memory.

## Gotchas
- Frustum culling still needs a far distance (or none): extract only 5 planes from the matrix; the far plane
  row is degenerate.
- Shadow cascades and fog cannot read "far" from the projection; keep a separate logical far distance.
- Code that assumes depth 1 = far (SSAO, sky masks, `depth == 1.0` tests) must flip to `depth == 0.0`.
- Post-processing that reconstructs position from depth must use the inverse of this matrix.

## Verify
(Computed here: the matrix above gives depth n/-z for z = -n, -1, -100, -1e6; the non-reversed infinite row `0 0 -1 -2n` gives -1 at the near plane; the finite reversed matrix gives 1 at near and 0 at far, and the linearisation formula in section 3 returned the original distance for 0.1, 5, 50 and 100.)
- [ ] Two coplanar-ish quads 1 cm apart at 10 km show no z-fighting; linearised depth matches view z within 0.1%.
