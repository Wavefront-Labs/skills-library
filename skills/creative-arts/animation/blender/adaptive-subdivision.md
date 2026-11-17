---
id: creative-arts.animation.blender.adaptive-subdivision
name: adaptive-subdivision
category: creative-arts
field: animation
product: blender
tags: [blender, adaptive-subdivision, dicing-rate, cycles, displacement, true-displacement, micropolygon]
level: practitioner
status: docs-checked
description: "Render true displacement in Cycles with adaptive subdivision: enabling it on the modifier, the Subdivision panel settings, and the material displacement method options."
sources:
  - https://docs.blender.org/manual/en/latest/render/materials/components/displacement.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/subdivision.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# adaptive-subdivision

Goal: terrain, rock and brick surfaces that get small polygons near the camera and few far away, with displacement from a texture in the material.

## Setup

1. Render engine Cycles.
2. Add a **Subdivision Surface** modifier and enable **Adaptive Subdivision** (Cycles only). Choose Adaptive Space: **Pixel** (target polygon pixel size) or **Object** (target edge length; required for instanced meshes).
3. Material Settings > **Displacement** method (per material): Bump Only, Displacement Only, or Displacement and Bump. The manual calls Displacement Only the most accurate and memory intensive, and says Displacement and Bump combines true displacement for large shapes with bump for fine detail, which can balance memory.
4. In the shader, connect a **Displacement** (or Vector Displacement) node to the Material Output's Displacement input, with a procedural, painted or baked texture driving it.

## Dicing settings (Render Properties > Subdivision)

- **Dicing Rate Render** / **Viewport**: multiplier for the size of micropolygons.
- **Offscreen Scale**: multiplier for dicing rate outside the camera view; higher uses less memory, lower improves off-screen reflections and shadows.
- **Max Subdivisions**: cap on the subdivision level.
- **Dicing Camera**: lock subdivision reference to one camera to avoid crawling when the scene camera moves.

## Gotchas

- Baked displacement: the manual says 16 or 32-bit float maps give the best results, as 8-bit often cannot represent the detail.
- Bump maps with image textures: use Cubic interpolation to avoid stepping.
- Once the mesh is subdivided very finely, the manual recommends true displacement only in Cycles; keeping bump just adds memory and render time.
- Cycles does not support unique displacement per instance.
- Instancing does not work well with Pixel space subdivision; use Object space.
- Memory grows quickly with tiny dicing rates on large surfaces, so loosen before tightening.

## Verify

Silhouettes are broken up by displacement (not just shading changes), render memory is reasonable, and comparing Displacement Only with Bump Only shows the geometry actually moving.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and the Cycles add-on source (ui.py on main).
Confirmed: modifier Adaptive Subdivision, Adaptive Space, Pixel Size, Edge Length; Subdivision panel settings; displacement methods and notes; float map and Cubic interpolation advice.
Removed as unconfirmed: the Experimental feature set step (absent from the 5.2 panel), "must be the last modifier" and the silent fallback claim, Midlevel values by map type, the 1.0 px default and the 4 to 25 offscreen range, the per-object Dicing Scale, and the claim that EEVEE ignores true displacement.
Method: documentation only; no commands were run.
