---
id: creative-arts.animation.blender.particle-texture-influence
name: particle-texture-influence
category: creative-arts
field: animation
product: blender
tags: [blender, particles, particle-texture-influence, particle-texture, density-texture]
level: practitioner
status: docs-checked
description: "Drive Blender particle time, lifetime, density, size, velocity and hair properties with textures in a particle Textures slot, with the available coordinate types."
sources:
  - https://docs.blender.org/manual/en/latest/physics/particles/texture_influence.html
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# particle-texture-influence

## Setup

Particle Properties > **Textures** panel > New texture. Edit it in the Texture properties tab (an Image texture or a procedural type such as Clouds). The Influence settings are in Texture > Influence.

## Influence

Per the manual, a texture can affect:
- **General**: Time (emission time), Lifetime, Density, Size.
- **Physics**: Velocity (initial), Damp, Gravity, Force Fields.
- **Hair**: Length (child hair), Clump, Kink, Rough.

The particle texture slot in the Python API also has kink amplitude and frequency and twist toggles (`use_map_kink_amp`, `use_map_kink_freq`, `use_map_twist`), so the exact Hair list in the UI may be longer than the manual's.

## Mapping (Texture Coordinates)

The API's `texture_coords` options are: Global, Object (the linked object's coordinates, so an animated object can act as a projector), UV, Generated (original undeformed coordinates), and Strand / Particle (normalised strand coordinate for hair, or particle age and trail position). The manual's page leaves mapping coordinates undocumented.

## Recipes

- Grass patches: a Clouds texture driving Density on a hair system.
- Disintegration: a gradient texture with Object coordinates from a moving empty, influencing Time, so particles emit as the gradient passes.

## Gotchas

- Image textures need UV coordinates selected, otherwise Generated or another mapping will not line up with the mesh.
- Vertex groups (Density, Length) are often simpler than textures for hair.

## Verify

The viewport emission pattern matches the texture, and moving the projector object shifts the emission front.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and rna_particle.cc on main.
Confirmed: Influence groups and their descriptions; Texture > Influence panel location; coordinate enum items from source.
Removed as unconfirmed: the "Blend mode (Multiply etc.)" claim, "density influence is threshold-like", and the Strand/Particle shorthand from the draft. The source URL was the manual's root and is replaced with the Texture Influence page.
Method: documentation only; no commands were run.
