---
id: creative-arts.animation.blender.cloth-stiffness-presets
name: cloth-stiffness-presets
category: creative-arts
field: animation
product: blender
tags: [blender, cloth, cloth-stiffness-presets, cloth-presets, cloth-stiffness, bending-stiffness, linear-vs-angular-bending, fabric-types]
level: practitioner
status: docs-checked
description: "Pick and tune Blender cloth material: presets menu, vertex mass, tension/compression/shear/bending stiffness, bending model, quality steps and scale-dependence."
sources:
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/index.html
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/physical_properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cloth-stiffness-presets

Goal: fabric that reads as the intended material. General cloth workflow is in `cloth-simulation`.

## Presets

The **Presets** menu at the top of Physics > Cloth holds ready-made cloth examples (the manual does not list them). Pick the closest, then tune one parameter at a time.

## Key parameters (Physical Properties)

- **Vertex Mass**: mass of the cloth material, applied per vertex. Total weight therefore depends on vertex count, so retune after subdividing.
- **Air Viscosity**: air drag (see `cloth-damping`).
- **Bending Model**: **Angular** (angular bending springs) or **Linear** (the old model with linear bending springs). **Structural** stiffness and damping appear only with Linear.
- **Stiffness**: **Tension** (resists stretching), **Compression** (resists compression), **Shear** (resists shearing), **Bending** (wrinkle coefficient; higher creates more large folds).
- **Damping** per stiffness type (see `cloth-damping`).
- Cloth is built from tension, compression, shear and angular bending springs that can be controlled independently.

## Quality and scale

- **Quality Steps** (top of Physics > Cloth): simulation steps per frame; higher is better and slower. Raise it for stiff materials or fast motion.
- Model at a realistic size and apply scale; the sim is scale-sensitive.
- Mesh resolution limits fold size: very low resolution cannot form fine folds.

## Gotchas

- Changing vertex count after tuning changes the feel because mass is per vertex.
- Very stiff settings with low Quality Steps tend to be unstable; raise steps before stiffness.

## Verify

Drop a test square of the cloth over a sphere: drape and fold size match your reference for the fabric.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Presets menu, Quality Steps, Vertex Mass, Air Viscosity, Bending Model (Angular and Linear) and the stiffness and damping field names. Removed the preset names, per-fabric stiffness numbers, the default bending model claim and typical edge length, none of which the manual states.
Method: documentation only; no commands were run.
