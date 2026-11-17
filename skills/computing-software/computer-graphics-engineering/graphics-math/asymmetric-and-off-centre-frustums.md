---
id: computing-software.computer-graphics-engineering.graphics-math.asymmetric-and-off-centre-frustums
name: asymmetric-and-off-centre-frustums
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, projection, asymmetric-frustum, off-axis-projection, stereo-projection, jitter, head-tracking]
level: advanced
status: draft
description: "Build off-centre (asymmetric) projection frustums: glFrustum-style matrices, head-tracked displays and CAVEs (Kooima), stereo with parallel axes, tiled rendering and TAA jitter."
sources: ["https://csc.lsu.edu/~kooima/articles/genperspective/", "https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glFrustum.xml", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Off-centre and asymmetric frusta

## General perspective matrix (GL convention)
For near-plane window `[l, r] x [b, t]` at distance n:
```
[2n/(r-l)   0        (r+l)/(r-l)    0         ]
[0          2n/(t-b) (t+b)/(t-b)    0         ]
[0          0        -(f+n)/(f-n)  -2fn/(f-n) ]
[0          0        -1             0         ]
```
Symmetric frusta have `r = -l, t = -b`, so the third-column terms vanish. Off-centre terms shift the
image without rotating the camera.

## Head-tracked displays / CAVE (Kooima)
Screen corners pa (lower-left), pb (lower-right), pc (upper-left) in tracker space, eye pe:
```
vr = normalize(pb - pa); vu = normalize(pc - pa); vn = normalize(cross(vr, vu))
va = pa - pe; vb = pb - pe; vc = pc - pe; d = -dot(va, vn)
l = dot(vr, va) * n / d; r = dot(vr, vb) * n / d; b = dot(vu, va) * n / d; t = dot(vu, vc) * n / d
P = frustum(l, r, b, t, n, f) * M^T(vr, vu, vn) * T(-pe)
```
The window looks like a real window into the scene as the head moves.

## Stereo
Use parallel cameras offset by +-IPD/2 with asymmetric frusta converging at the screen/zero-parallax
distance. Toe-in (rotating cameras inward) causes vertical parallax and eye strain. XR runtimes give
per-eye asymmetric FOV angles (`XrFovf` left/right/up/down tangents): build the matrix from tangents
directly.

## Sub-pixel jitter (TAA, supersampling)
Offset the projection by a fraction of a pixel: add `jx * 2 / width` and `jy * 2 / height` to
`P[2][0]` and `P[2][1]` (column-major, the terms multiplied by z). Halton(2,3) sequences are typical.

## Tiled/multi-monitor
Split one frustum into tiles by sub-dividing `[l, r] x [b, t]`; each tile is an asymmetric frustum,
images line up seamlessly.

## Verify
Render a grid through split tiles and stitched output must match a single full render pixel for pixel.
