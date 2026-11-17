---
id: creative-arts.animation.blender.field-weights
name: field-weights
category: creative-arts
field: animation
product: blender
tags: [blender, force-fields, field-weights, effector-collection, gravity]
level: practitioner
status: docs-checked
description: "Control which force fields affect each Blender simulation via Field Weights: gravity, per-type multipliers and effector collections."
sources:
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/field_weights.html
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/field_weights.html
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/force_field.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# field-weights

## Where they are

A Field Weights panel controls how much each force field type affects a simulation. It exists for particle systems, Cloth, Soft Body, the Rigid Body World, Fluid domains and the Dynamic Paint Drip effect.

## Settings

- **Effector Collection**: only force fields in this collection affect the simulation; the manual calls the particle version Effector Group.
- **Gravity**: how much the global gravity affects the simulation.
- **All**: scales all effector weights.
- Per-type weights: Force, Vortex, Magnetic, Harmonic, Charge, Lennard-Jones, Wind, Curve Guide, Texture, Fluid Flow (not shown on fluid domains), Turbulence, Drag, Boid.

## Patterns

- Shot with fire and a flag: put the wind in a collection `flag_fx`, set the flag cloth's Effector Collection to it, and give the smoke domain a different collection.
- To remove a simulation from the influence of one field type, turn that type's weight down in its Field Weights panel.

## Gotchas

- Force fields affect everything by default; use the weights or an Effector Collection to limit them.
- Particle systems can also generate force fields (Particle System > Force Field Settings); **Self Effect** makes those fields affect other particles in the same system.
- After changing field settings you may need to Free Cache on particle, soft body or cloth systems; this is not automatic.

## Verify

Set one type's weight to 0 on one simulation: that simulation stops reacting to that type while others keep reacting.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/cloth/settings/field_weights, physics/fluid/type/domain/field_weights, physics/particles/emitter/force_field and physics/forces/force_fields/introduction; branch blender-v5.2-release) and the 5.2 source (rna_object_force.cc, properties_physics_common.py). Confirmed: Field Weights panels per system, Effector Collection/Group, Gravity, All, per-type weights, Self Effect, and the Free Cache note.

Method: documentation only; no commands were run.
