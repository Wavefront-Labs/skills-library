---
id: computing-software.computer-graphics-engineering.rendering-techniques.g-buffer-packing-layouts
name: g-buffer-packing-layouts
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, efficient-shading, gbuffer-packing, deferred-shading, octahedral-normals, render-targets, bandwidth]
level: advanced
status: draft
description: "Design compact G-buffer layouts: packing normals (octahedral), roughness, metallic, material IDs and flags into RGBA8/RGB10A2 targets, bandwidth per pixel and decoding cost."
sources: ["https://jcgt.org/published/0003/02/01/", "https://aras-p.info/texts/CompactNormalStorage.html", "https://advances.realtimerendering.com/s2016/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# G-buffer packing layouts

## 1. Budget
G-buffer bandwidth = width x height x bytes per pixel x (write + reads). At 1440p, 4 RGBA8 targets +
D32S8 = 20 B/px = 74 MB written per frame before lighting reads. Every byte saved matters on
consoles and mobile.

## 2. Typical layout (UE/Frostbite-like)
| Target | Format | R | G | B | A |
|---|---|---|---|---|---|
| GB0 | RGBA8 sRGB | albedo R | albedo G | albedo B | AO / spec occlusion |
| GB1 | RGB10A2 | normal oct X | normal oct Y | roughness | material ID bits (2) |
| GB2 | RGBA8 | metallic | specular (F0 scale) | custom data (SSS, clearcoat) | shading model ID |
| Velocity | RG16F | motion x | motion y | | |
| Depth | D32 (reversed-Z) + stencil | | | | |

## 3. Normal encoding
- **Octahedral** (Cigolle et al. 2014): unit vector -> 2 components, good precision in 2x10 or 2x12
  bits; cheap encode/decode:
```glsl
vec2 octWrap(vec2 v) { return (1.0 - abs(v.yx)) * vec2(v.x >= 0.0 ? 1.0 : -1.0, v.y >= 0.0 ? 1.0 : -1.0); }
vec2 encodeOct(vec3 n) { n /= (abs(n.x) + abs(n.y) + abs(n.z)); n.xy = n.z >= 0.0 ? n.xy : octWrap(n.xy); return n.xy * 0.5 + 0.5; }
vec3 decodeOct(vec2 f) { f = f * 2.0 - 1.0; vec3 n = vec3(f, 1.0 - abs(f.x) - abs(f.y));
    float t = clamp(-n.z, 0.0, 1.0); n.xy += vec2(n.x >= 0.0 ? -t : t, n.y >= 0.0 ? -t : t); return normalize(n); }
```
- Avoid storing XYZ in RGB8 (wastes 1/3, poor precision) or view-space XY with reconstructed Z
  (breaks for normals facing away with perspective).

## 4. Packing tricks
- Bit-pack small fields (shading model ID 3-4 bits, flags) into alpha or into the low bits of a
  10/16-bit channel with `packUnorm`/bit ops; use `R32_UINT` targets for maximum packing control.
- Store roughness in perceptual space (better 8-bit distribution).
- YCoCg chroma subsampling across a checkerboard (Mavridis & Papaioannou) halves albedo storage.
- Reconstruct position from depth; never store it.

## 5. Visibility buffer alternative
Store only triangle ID + instance ID (32-64 bits) and re-evaluate attributes in the lighting pass:
minimal bandwidth, independent of material complexity.

## Gotchas
- Blending into packed targets (decals) breaks bit-packed fields; keep decal-modified data in
  blendable channels.
- sRGB target for albedo only; data targets must be linear (UNORM).
- MSAA multiplies G-buffer size; packing matters even more.

## Verify
- [ ] Encode/decode round-trip error measured for normals (max angular error).
- [ ] Bandwidth per frame computed and compared to budget; G-buffer debug views decode correctly.
