---
id: computing-software.computer-graphics-engineering.rendering-techniques.lightmap-uv-unwrapping-and-seams
name: lightmap-uv-unwrapping-and-seams
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, global-illumination, lightmap-uvs, xatlas, uv-unwrapping, lightmap-seams, uv2, texel-density]
level: practitioner
status: docs-checked
description: "Generate lightmap UVs that bake cleanly: unwrapping with xatlas, chart padding, texel density, and fixing seams, leaks and bleeding in the baker."
sources: ["https://github.com/jpcy/xatlas", "https://ndotl.wordpress.com/2018/08/29/baking-artifact-free-lightmaps/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lightmap UV unwrapping and seams

## 1. Requirements of lightmap UVs (UV2)
- Unique texture coordinates: charts must not overlap (unlike material UVs, which may tile or
  mirror). xatlas is "a small C++11 library with no external dependencies that generates unique
  texture coordinates suitable for baking lightmaps or texture painting".
- Leave space around charts for the texels bilinear filtering will sample.
- Meshes are split into charts, which are parameterised and packed into an atlas.

## 2. xatlas (simple API)
```cpp
xatlas::Atlas* atlas = xatlas::Create();
xatlas::MeshDecl m; m.vertexCount = n; m.vertexPositionData = pos; m.vertexPositionStride = 12;
m.indexCount = ic; m.indexData = idx; m.indexFormat = xatlas::IndexFormat::UInt32;
xatlas::AddMesh(atlas, m);                 // returns an AddMeshError
xatlas::PackOptions po; po.padding = 4; po.texelsPerUnit = 10.0f; po.bilinear = true;
xatlas::Generate(atlas, xatlas::ChartOptions{}, po);
// atlas->meshes[0].vertexArray[i].uv and .xref, atlas->width / atlas->height
xatlas::Destroy(atlas);
```
- Output meshes have more vertices (the UV channel adds seams) but the same number of indices.
  `xref` is the index of the input vertex an output vertex came from; use it to copy other
  attributes.
- `PackOptions`: `padding` (pixels to pad charts with), `texelsPerUnit` (a 1x1 quad at 32 takes
  about 32x32 texels; 0 estimates a value to match `resolution`, or about a 1024x1024 atlas if
  both are 0), `resolution` (0 gives one atlas sized by texelsPerUnit), `bilinear` (default
  true), `blockAlign` (align charts to 4x4 blocks, also faster packing), `bruteForce` (slower
  but best result, else random placement) and `maxChartSize`.
- `MeshDecl` can carry `faceMaterialData`; only faces with the same material go in one chart.
- Tool integration: call `ComputeCharts` then `PackCharts` separately, and call `PackCharts`
  repeatedly to tweak texels-per-unit and resolution.

## 3. Baker-side artefact fixes (ndotl.wordpress "Baking artifact-free lightmaps")
Post-dilating a rasterised UV G-buffer is not enough: very small triangles are skipped or
aliased. Use or emulate conservative rasterisation. The author renders the UV layout several
times with sub-pixel offsets (larger offsets first), with the unmodified centred G-buffer last,
rather than repurposing MSAA samples (whose off-centre samples caused more shadow leaking).

- **Shadow leaks**: texels are large, so a single lit point is interpolated over a big area.
  Trace at least 4 tangential rays from the texel centre, length half the world-space texel size;
  if a ray hits a backface the texel leaks, so push the centre out with
  `newPos = oldPos + rayDir * hitDistance + hitFaceNormal * bias`. Estimate world texel size from
  `ddx`/`ddy` of world position while rasterising the G-buffer.
- **Ray bias far from origin**: a constant epsilon breaks at large coordinates. The author uses
  `position += position * 0.0000002` (about FLT_EPSILON), or
  `position += sign(normal) * abs(position * 0.0000002)` for a directional bias.
- **Shadow terminator**: faceted geometry with smooth normals self-shadows wrongly; constant bias
  trades this against peter-panning, and blurring harms shadow width.
- **UV seams**: the Last of Us lighting talk used least squares to match texels across a seam.
  The post instead finds seam edges on the CPU (matching position and normal, differing UV),
  draws them as lines that copy the opposite side's colour, and ping-pongs two render targets
  until the sides match. Mip-mapping cannot be used when reading the lightmap here.
- seamoptimizer (linked from the xatlas README) is a single-file C/C++ library that minimises
  hard transition errors of disjoint edges in lightmaps.

## Gotchas
- Mirrored or overlapping UV2 corrupts bakes; validate overlap.
- Charts smaller than a texel can be skipped by rasterisation.

## Verify
- [ ] Overlap check passes and padding covers the bilinear footprint at the target resolution.
- [ ] No visible seam lines on curved surfaces and no dark bleed at chart edges after baking.

## Checked

Method: docs-checked 2026-11-09 against the xatlas README and xatlas.h (PackOptions and MeshDecl comments), and the ndotl.wordpress post (leaks, bias, terminator and seams sections read). Dropped the Unity import option (page not read), Blender tools, the 2/4-texel padding rule, the texel-density numbers and the claim that dilation alone pads charts.
