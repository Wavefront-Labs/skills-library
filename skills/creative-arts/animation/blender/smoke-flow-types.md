---
id: creative-arts.animation.blender.smoke-flow-types
name: smoke-flow-types
category: creative-arts
field: animation
product: blender
tags: [blender, smoke, fire, smoke-flow-types, flow-source, flow-type, particle-flow]
level: practitioner
status: docs-checked
description: "Choose Mantaflow gas flow types (smoke, fire, fire+smoke) and sources (mesh volume/surface, particles), plus density, temperature and texture."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/flow.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# smoke-flow-types

## Flow Type

- **Smoke**: emit only smoke. **Fire**: emit only fire (the domain still creates some smoke for burnt fuel). **Fire + Smoke**: both. **Liquid** for liquid domains.
- **Flow Behavior**: Inflow (continuous), Geometry (mesh becomes fluid), Outflow (remove). **Use Flow** applies to Inflow and Outflow only.

## Flow Source

- **Mesh**: emits from the mesh. **Surface Emission** is the maximum distance in voxels from the surface (results depend on domain resolution); **Volume Emission** (0 to 1) emits inside the mesh and is unpredictable on non-manifold meshes; **Is Planar** for planes and non-manifold meshes.
- **Particle System** (Fire or Smoke only; Emitter type particle systems only): particles emit. **Set Size** enables a **Size** giving the maximum distance in voxels at which particles emit smoke; without it each particle fills the nearest voxel.
- Other settings: **Density** (smoke emitted at once), **Initial Temperature**, **Fuel** (fire), **Smoke Color** (different colours blend), **Absolute Density**, **Vertex Group** to control where smoke is emitted.
- **Texture**: use a texture to control where on the mesh smoke or fire is emitted, with **Mapping** (Generated UVs or manual UV), **Size** and **Offset** (translates the texture along Z). It has no effect on Outflow.

## Recipes

- Chimney: Mesh source, Smoke, Inflow, a warm Initial Temperature and a clouds texture for patchy emission.
- Debris smoke trails: a particle system on fractured pieces as the flow source.
- Burning object: Fire, a Surface Emission distance, and a texture for uneven fire.

## Gotchas

- Flow objects must be inside the domain's bounding box.
- Use Flow must be on at the frames where you want emission.
- Particle-source flows only emit while the particles exist.
- Fire with a high Reaction Speed in the domain gives small flames (see fire-settings).

## Verify

Viewport smoke appears from the intended surfaces only; texture emission shows patchy distribution.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/flow; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Flow Type options, Flow Behavior, Use Flow scope, Mesh source options (Is Planar, Surface Emission, Volume Emission), Particle System restrictions and Set Size, Density, Initial Temperature, Fuel, Smoke Color, Absolute Density, Vertex Group, Texture panel (Mapping, Size, Offset along Z, no effect on Outflow).

Method: documentation only; no commands were run.
