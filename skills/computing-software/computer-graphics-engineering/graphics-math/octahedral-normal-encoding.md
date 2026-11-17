---
id: computing-software.computer-graphics-engineering.graphics-math.octahedral-normal-encoding
name: octahedral-normal-encoding
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, geometric-encoding, octahedral-encoding, normal-packing, g-buffer-normals, unit-vector-compression, oct16, snorm]
level: practitioner
status: verified
description: "Pack unit normals into two channels with octahedral encoding for G-buffers and vertex data: encode/decode code, precision per bit depth, sign handling."
sources: ["https://jcgt.org/published/0003/02/01/paper.pdf", "https://knarkowicz.wordpress.com/2014/04/16/octahedron-normal-vector-encoding/", "Akenine-Moller et al., Real-Time Rendering (4th ed.), ch. 16.6"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Octahedral normal encoding

**Goal:** store unit vectors in 2 components (16–32 bits total) with near-uniform error —
for G-buffers, compressed vertex normals/tangents and direction textures (Cigolle et al., JCGT 2014).

## 1. Idea
Project the unit sphere onto an octahedron (L1 normalisation), unfold the lower half over the
upper half's corners, and you get a square [-1,1]². Error is far more uniform than storing
xy and reconstructing z, or spherical angles.

## 2. Code
```glsl
vec2 octWrap(vec2 v) { return (1.0 - abs(v.yx)) * vec2(v.x >= 0.0 ? 1.0 : -1.0, v.y >= 0.0 ? 1.0 : -1.0); }
vec2 octEncode(vec3 n) {                       // n must be normalised
    n /= (abs(n.x) + abs(n.y) + abs(n.z));
    vec2 p = n.z >= 0.0 ? n.xy : octWrap(n.xy);
    return p * 0.5 + 0.5;                      // to [0,1] for UNORM targets (skip for SNORM)
}
vec3 octDecode(vec2 f) {
    f = f * 2.0 - 1.0;
    vec3 n = vec3(f.x, f.y, 1.0 - abs(f.x) - abs(f.y));
    float t = max(-n.z, 0.0);
    n.x += n.x >= 0.0 ? -t : t;                // branch-free fold (Rune Stubbe variant)
    n.y += n.y >= 0.0 ? -t : t;
    return normalize(n);
}
```
Note the sign helper: GLSL `sign(0) = 0` breaks the wrap for components exactly zero — use the
explicit `>= 0` select as above.

## 3. Precision by storage
| format | max angular error (approx.) | use |
|---|---|---|
| RG8 (16 bit) | ~0.94° (measured) | low-end, mobile G-buffers (visible banding on smooth specular) |
| RG16 UNORM/SNORM (32 bit) | ~0.004° (measured) | high-quality G-buffers, vertex normals |
| 2×10 bits (e.g. RGB10A2) | ~0.23° (measured) | packed G-buffers |
For 8-bit, "precise" encoding (search neighbouring quantised values for the best decode) cuts
error noticeably at encode-time cost.

## 4. Where it's used
- G-buffer normals (deferred rendering) — frees channels for roughness/material IDs.
- Vertex normal + tangent compression (tangent can be encoded as an angle relative to the
  normal's frame, or also octahedral).
- Octahedral maps for environment/probe textures and impostor view directions.

## Gotchas
- Filtering/blending encoded normals (MSAA resolve, bilinear) gives wrong results near the fold
  — decode first, or point-sample.
- Encode only normalised vectors; normalise after decode.
- SNORM vs UNORM: SNORM has an exact zero but -1 and -1+ulp both map to -1.0.

## Verify
- [ ] Round-trip error over a dense sphere sampling below the target for the chosen format.
- [ ] Specular highlights on smooth spheres free of banding at the chosen bit depth.
- [ ] Unit tests include axis-aligned vectors and components exactly zero.
