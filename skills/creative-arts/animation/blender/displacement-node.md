---
id: creative-arts.animation.blender.displacement-node
name: displacement-node
category: creative-arts
field: animation
product: blender
tags: [blender, shader, displacement-node, vector-displacement, true-displacement, adaptive-subdivision]
level: practitioner
status: docs-checked
description: "Set up true displacement in Blender materials: Displacement and Vector Displacement nodes, midlevel, scale, material displacement method and subdivision."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/displacement/displacement.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/displacement/vector_displacement.html
  - https://docs.blender.org/manual/en/5.2/render/materials/components/displacement.html
  - https://docs.blender.org/manual/en/5.2/render/cycles/material_settings.html
  - https://docs.blender.org/manual/en/5.2/render/eevee/material_settings.html
  - https://docs.blender.org/manual/en/5.2/modeling/modifiers/generate/subdivision_surface.html
  - https://developer.blender.org/docs/release_notes/4.2/eevee/
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# displacement-node

## Nodes

- **Displacement**: inputs **Height**, **Midlevel** (neutral value that gives no displacement; default 0.5, lower values push inwards, higher outwards), **Scale**, **Normal**. Property **Space**: Object (displacement scales with the object) or World (object scale ignored). Output **Displacement** goes to Material Output Displacement.
- **Vector Displacement**: input **Vector** (typically a baked vector displacement image), **Midlevel** (default 0.0), **Scale**. Space Object (RGB read as an XYZ offset; fine for static meshes) or Tangent (R along tangent, G along normal, B along bitangent; for deforming meshes). Displaces along arbitrary directions, so it can represent overhangs.

## Material setting

Material Properties > Settings > Surface > **Displacement** (Cycles; EEVEE has the same setting): **Bump Only** (shading normal only), **Displacement Only** (true displacement, most accurate and most memory), **Displacement and Bump**. By default Blender uses bump mapping only, so change this to see real displacement. In EEVEE, Displacement Only falls back to Displacement and Bump.

## Geometry resolution

- True displacement needs a finely subdivided mesh.
- Cycles **Adaptive Subdivision** (Subdivision Surface modifier, Cycles only) subdivides by distance to the camera; Adaptive Space is Pixel (target pixel size) or Object (target edge length, needed for instanced meshes). Instancing works poorly with Pixel space.
- EEVEE supports displacement from 4.2 onwards; its Max Distance setting limits how far a vertex may move, and larger displacements can cause visibility and shadow issues.

## Gotchas

- Baked displacement maps look best at 16 or 32-bit float; 8-bit images often cannot hold the detail. Bump maps should use Cubic image interpolation to avoid stepping.
- Cycles does not support unique displacement per instance.
- Once the mesh is very finely subdivided, drop the bump part in Cycles: it only costs memory and render time.

## Verify

Silhouette shows real detail with Displacement Only or Displacement and Bump; with Bump Only the outline does not change.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against displacement/displacement, displacement/vector_displacement, materials/components/displacement, the Cycles and EEVEE material settings pages, the Subdivision Surface page (adaptive) and the 4.2 EEVEE release notes (displacement support). Removed the Experimental feature set and Dicing Rate steps (not in the 5.2 manual), the 3-6 subdivision levels, the ZBrush/Substance midlevel advice, the Non-Color remark, seam-crack and sculpt-scale claims.

Method: documentation only; no commands were run.
