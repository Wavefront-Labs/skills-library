---
id: computing-software.computer-graphics-engineering.rendering-techniques.lightmap-baking
name: lightmap-baking
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, global-illumination, lightmaps, lightmap-baking, uv2-unwrap, directional-lightmaps, lightmap-uvs, xatlas]
level: advanced
status: draft
description: "Bake lightmaps: second UV unwrap with xatlas, texel density, path-traced baking, dilation and seams, directional or SH lightmaps, and runtime encoding."
sources: ["https://github.com/jpcy/xatlas", "https://www.realtimerendering.com/", "https://docs.unity3d.com/Manual/Lightmappers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lightmap baking

## 1. UV2
- Unique, non-overlapping UVs per static mesh (xatlas: `xatlas::Generate` with padding).
- Padding of 2-4 texels at the lowest used resolution; chart borders bleed otherwise.
- Texel density in texels per metre (e.g. 10-40 indoors); scale per object for importance.

## 2. Bake
- For each lightmap texel, compute world position and normal (rasterise UV2 triangles into a
  position/normal G-buffer at lightmap resolution, with conservative rasterisation for thin
  triangles).
- Path trace from each texel (hemisphere sampling, several bounces, direct lights with MIS) on
  GPU (OptiX, Embree on CPU, or DXR/Vulkan RT). Denoise with OIDN (lightmap mode).
- Bias ray origins along the normal to avoid self-intersection; texels inside geometry
  (backface hit first) are invalid: mark and fill.

## 3. Post-process
- **Dilate** valid texels into empty space several times so bilinear filtering at chart edges
  has data.
- Seam stitching: match texels on both sides of UV seams (least squares) to hide lines.

## 4. Runtime formats
| Type | Gives |
|---|---|
| Irradiance (RGB HDR) | Diffuse only, flat look on normal maps |
| Directional (dominant dir + colour) | Normal-map response |
| SH L1 lightmaps (4 coeffs) | Best normal response, also approximate specular |
Encode as BC6H, RGBM/RGBE in BC3, or half-float; apply exposure consistently.

## Gotchas
- Dynamic objects need light probes (SH grid) matching the lightmaps.
- Light leaking under walls: thin geometry, texels sampling from both sides; add thickness or
  increase density.
- Rebake after any static geometry change; automate in the build.

## Verify
- [ ] Lightmap texel-density view uniform; no seams or black chart edges.
