---
id: computing-software.computer-graphics-engineering.rendering-techniques.visibility-buffer-rendering
name: visibility-buffer-rendering
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, visibility-buffer, deferred-texturing, triangle-id, gpu-driven-rendering, material-classification]
level: sme
status: draft
description: "Build a visibility-buffer renderer: write triangle and instance IDs, reconstruct attributes and derivatives analytically, and classify materials for shading."
sources: ["https://jcgt.org/published/0002/02/04/", "https://www.conffx.com/Visibility_Buffer_GDCE.pdf", "https://advances.realtimerendering.com/s2021/Karis_Nanite_SIGGRAPH_Advances_2021_final.pdf", "http://filmicworlds.com/blog/visibility-buffer-rendering-with-material-graphs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Visibility buffer

## 1. Idea
Rasterise once into a 32- or 64-bit target holding only `(instanceID, triangleID)` (plus depth). Shading
happens later per pixel: fetch the triangle's vertices, reconstruct barycentrics, interpolate attributes, run
the material. Bandwidth is tiny compared with a fat G-buffer and quad overshading on small triangles is cut.

## 2. Visibility pass
```hlsl
uint main(uint primID : SV_PrimitiveID, nointerpolation uint inst : INSTANCE) : SV_Target {
  return (inst << 7) | (primID & 0x7F);    // or pack cluster/meshlet id + local triangle id
}
```
Pick the packing from your counts (e.g. 25 bits cluster, 7 bits triangle in a meshlet of <=128).
With 64-bit atomics (`InterlockedMax` on `depth<<32 | id`) a compute rasteriser can write the same buffer.

## 3. Attribute reconstruction
- Transform the 3 vertices to clip space, compute barycentrics of the pixel centre perspective-correctly
  (Schied and Dachsbacher), and their screen-space partial derivatives analytically.
- Interpolate UVs and their derivatives with the same barycentric derivatives and use `SampleGrad`; implicit
  derivatives are meaningless in a full-screen/compute pass.
- Normals/tangents interpolate the same way; skinned meshes need post-skinning positions (store them, or re-skin).

## 4. Material shading
- Classify: tile pass builds per-material pixel lists (or a material-ID depth buffer drawn as full-screen
  quads with depth-equal test, as in Nanite), then dispatch one shading pass per material over its tiles.
- Uber-shader with a switch is simple but suffers divergence and register pressure.

## Gotchas
- Alpha-tested geometry must evaluate the alpha in the visibility pass (needs UVs there).
- MSAA: store per sample, or use TAA only.
- Index buffer and vertex fetch must be accessible in the shading pass: bindless or a single big buffer.

## Verify
- [ ] Debug view coloured by triangle ID matches the raster; texture LOD visually equals forward rendering
  (compare mip-level debug colours).
- [ ] GPU profile shows lower bandwidth than the G-buffer path on dense geometry.
