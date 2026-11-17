---
id: computing-software.computer-graphics-engineering.rendering-techniques.procedural-vs-baked-textures
name: procedural-vs-baked-textures
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, texturing, baked-textures, procedural-textures, texture-baking, substance-designer, shader-optimisation]
level: practitioner
status: draft
description: "Decide between procedural shader textures and baked bitmaps: cost per pixel vs memory/bandwidth, resolution independence, filtering/aliasing, authoring workflow and hybrid baking."
sources: ["https://www.adobe.com/products/substance3d/apps/designer.html", "https://thebookofshaders.com/11/", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Procedural vs baked texture trade-offs

## 1. Comparison
| | Procedural (in shader) | Baked (bitmap) |
|---|---|---|
| Runtime cost | ALU per pixel, grows with octaves/layers | 1 fetch, near constant |
| Memory | ~0 | width x height x bpp (BC compressed) |
| Resolution | infinite detail | fixed; blurs or tiles up close |
| Filtering | must handle antialiasing yourself (no mips) | hardware mipmapping/aniso |
| Variation | unbounded, no tiling | tiles unless hidden |
| Authoring | code/graphs | painting, scans, Substance |

## 2. When procedural wins
- Huge surfaces needing non-repeating variation (terrain macro variation, sky, water).
- Parameters animated at runtime (dissolve, wetness masks, damage).
- Memory-starved targets with spare ALU (rare on mobile: bandwidth and ALU both tight).
- Dynamic UI shapes (SDF), stylised patterns.

## 3. When baked wins
- Anything with complex detail (scans, painted art).
- Shaders already ALU-bound.
- Need for stable mipmapped filtering at distance.

## 4. Hybrid
- **Bake procedural graphs** to textures offline (Substance Designer, Houdini COPs, a compute pass
  at load time). Get the authoring benefits without per-pixel cost.
- **Runtime baking**: generate noise/terrain textures once at load or into a virtual texture page
  cache (RVT in UE) when needed.
- **Small baked noise + procedural combination**: a 256^2 tileable noise texture sampled at several
  scales replaces most ALU noise cheaply.

## 5. Antialiasing procedural patterns
Use `fwidth` to band-limit: fade high-frequency octaves when their period is smaller than a pixel
(`amp *= smoothstep(1.0, 0.5, freq * fwidth(p))`), or integrate the pattern over the pixel footprint
for stripes/checkers (box-filtered checker formula from Quilez).

## Gotchas
- Procedural noise in fp16 shows artefacts at large coordinates.
- Baked textures need consistent texel density and compression choice; budget review per platform.

## Verify
- [ ] GPU time and memory compared for both approaches on the target device.
- [ ] Procedural patterns don't alias at distance.
