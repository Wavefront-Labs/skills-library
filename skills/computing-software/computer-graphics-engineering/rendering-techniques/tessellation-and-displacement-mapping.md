---
id: computing-software.computer-graphics-engineering.rendering-techniques.tessellation-and-displacement-mapping
name: tessellation-and-displacement-mapping
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, geometry-processing, displacement-mapping, tessellation, hull-shader, domain-shader, relief-mapping, cone-step-mapping]
level: advanced
status: docs-checked
description: "Direct3D 11 hardware tessellation (hull, tessellator, domain stages and factor ranges) and per-fragment displacement with relaxed cone stepping as the no-geometry alternative."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d11/direct3d-11-advanced-stages-tessellation", "https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-18-relaxed-cone-stepping-relief-mapping"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tessellation and displacement mapping

Two ways to add surface detail from a low-detail model: hardware tessellation that really adds
geometry, and per-fragment ray-height-field tracing that adds none.

## 1. Direct3D 11 tessellation pipeline
Tessellation turns low-detail patches (quad, triangle or isolines) into many smaller triangles,
points or lines using tessellation factors. Benefits per the docs: less memory and bandwidth,
displacement mapping, continuous or view-dependent level of detail computed on the fly, and
expensive work (blend shapes, morph targets, skinning) done at the lower detail.

Three stages:
- **Hull shader** (programmable, once per patch): input and output are each 1 to 32 control points.
  It declares the state the tessellator needs (control point count, patch face type, partitioning)
  and outputs tessellation factors. Internally it has a control-point phase (once per control
  point) and a patch-constant phase (once per patch, makes edge factors and other constants).
  If any edge factor is 0 or NaN the patch is culled: the domain shader does not run and nothing
  is drawn for it. Use this to cull off-screen or back-facing patches.
- **Tessellator** (fixed function): tiles a canonical normalised domain (a quad becomes a unit
  square) from the factors and the partitioning type, and outputs uv (and optionally w)
  coordinates and topology. Factor processing uses 32-bit float; point generation uses 16-bit
  fractional fixed point (the docs give 2 mm resolution on a 64 m patch as an example).
- **Domain shader** (programmable, once per tessellator output point): computes the vertex
  position from the uv, hull control points, patch constants and tessellation factors. The
  factors it receives include raw values before integer rounding, which helps geomorphing.
  This is where you sample a height map and displace.

Partitioning and factor ranges: `fractional_odd` [1..63], `fractional_even` [2..64], `integer`
[1..64], `pow2` [1..64].

Setup: shaders use shader model 5 (`hs_5_0`, `ds_5_0`), created with `CreateHullShader` and
`CreateDomainShader` and bound with `HSSetShader` and `DSSetShader`. Binding a hull shader sets
up the tessellator. The input assembler must supply patch topologies (`IASetPrimitiveTopology`
with a patch-constant topology). Set the hull and domain shaders to NULL to disable tessellation.
A geometry shader expecting adjacency primitives is invalid with tessellation active.

## 2. Crack-free edges
The pages do not give a recipe; the principle that follows from the stage design is that the
edge factors come out of the patch-constant phase, so compute each shared edge's factor from that
edge's data only, so both neighbouring patches agree. Check for cracks visually.

## 3. Alternative: relaxed cone stepping (GPU Gems 3, ch. 18)
Per-fragment displacement changes no geometry (so silhouettes are not displaced unless extra
steps are taken). Relief mapping finds the ray-height-field intersection with a linear search then
a binary search; the linear search can alias on thin structures. Cone step mapping uses a cone map
(a cone per depth texel) to leap safely but tends to stop before the surface at a capped iteration
count. Relaxed cone stepping widens the cones so a ray can pierce the surface at most once, then
finishes with a binary search.
- Store the depth map and cone ratio together (for example a luminance-alpha texture, or the cone
  in the blue channel of a relief texture); separating depth and normal into two textures
  compresses and caches better.
- Relaxed cone maps are made offline with an O(n squared) algorithm; the chapter clamps cone
  ratios to 1.0 to allow integer textures.
- The chapter's sample uses 15 cone steps and 6 binary steps and says 15 relaxed cone steps seem
  sufficient for typical height fields.
- Do not mipmap cone maps normally; take the minimum per pixel group when building mips, or
  sample the cone map with nearest neighbour.

## Verify
Wireframe overlay to check density against distance; look for cracks against a bright background;
profile the tessellation stages on target hardware.

## Checked
Checked 2026-11-08 against the Direct3D 11 Tessellation Stages page and GPU Gems 3 chapter 18.
Removed because those pages do not state them (and the Khronos OpenGL wiki page was blocked to
the reader): the GLSL tessellation control and evaluation shader code, the 8 to 16 pixel target
edge length, the claim that high factors are slow on many GPUs, and the mesh shader and Nanite
alternatives.
Method: docs-only read of cited pages, 2026-11-08
