---
id: computing-software.computer-graphics-engineering.graphics-math.uv-unwrapping
name: uv-unwrapping
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [computer-graphics-engineering, graphics-math, geometry-processing, uv-unwrapping, xatlas, texture-atlas, lightmap-uvs, parameterization]
level: practitioner
status: draft
description: "Generate UVs for texturing and lightmaps: seams and charts, distortion metrics, xatlas automatic atlases, packing with padding, texel density and lightmap UV rules."
sources: ["https://github.com/jpcy/xatlas", "https://docs.blender.org/manual/en/latest/modeling/meshes/editing/uv.html", "https://docs.unity3d.com/Manual/LightingGILightmapUVs.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UV unwrapping

## Concepts
- **Seams** cut the surface into charts that can be flattened; each chart maps to a region of UV
  space.
- **Distortion**: angle (conformal, LSCM) vs area (stretch); minimising both needs more seams.
- **Packing**: arrange charts in [0,1]^2 with padding (gutter) so mip-mapping/bilinear filtering
  does not bleed between charts.

## xatlas (automatic)
```cpp
xatlas::Atlas* atlas = xatlas::Create();
xatlas::MeshDecl decl;
decl.vertexPositionData = positions; decl.vertexPositionStride = sizeof(float) * 3; decl.vertexCount = vcount;
decl.indexData = indices; decl.indexCount = icount; decl.indexFormat = xatlas::IndexFormat::UInt32;
xatlas::AddMesh(atlas, decl);
xatlas::PackOptions po; po.resolution = 1024; po.padding = 4; po.bilinear = true;
xatlas::Generate(atlas, xatlas::ChartOptions(), po);
// atlas->meshes[0].vertexArray[i].uv and .xref (original vertex index): vertices are split at seams
xatlas::Destroy(atlas);
```
Python: `pip install xatlas`; `vmapping, indices, uvs = xatlas.parametrize(verts, faces)`.

## Lightmap UVs
- No overlaps, all UVs inside [0,1], padding sized for the lowest lightmap resolution (in texels, e.g.
  2 to 4 texels at the final lightmap size).
- Uniform texel density across the mesh; keep seams in hidden places.
- Engines can generate them (Unity "Generate Lightmap UVs", Unreal lightmap UV channel).

## Texture UVs (artist workflow)
Mark seams along natural edges, unwrap (angle-based or conformal), straighten rectangular parts,
check with a checker texture, pack with consistent texel density (e.g. 10.24 px/cm for a game
standard), and mirror/overlap symmetric parts to save space where lightmaps are separate.

## Verify
Checker texture: squares should be square and similar size everywhere; count overlapping UV faces
(must be zero for lightmaps); inspect mip levels for seam bleeding.
