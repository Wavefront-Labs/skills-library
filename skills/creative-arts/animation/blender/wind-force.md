---
id: creative-arts.animation.blender.wind-force
name: wind-force
category: creative-arts
field: animation
product: blender
tags: [blender, force-fields, wind-force, wind-force-field, wind, noise]
level: practitioner
status: docs-checked
description: "Set up Blender wind force fields: strength, direction, noise, flow, falloff and shape for cloth, hair, particles and smoke."
sources:
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/introduction.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/wind.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# wind-force

## Create

Add > Force Field > Wind (an empty with the field attached). Wind gives a constant force in one direction along the force object's local Z axis; the strength is shown by the spacing of the circles. Rotate the empty to aim it. New wind fields default to the Plane shape.

## Settings

- **Strength**: magnitude of the force; positive or negative changes direction, and it scales with the object's scale.
- **Flow**: if nonzero, adds a drag proportional and opposite to the point velocity, so Strength to Flow defines an air-flow velocity and objects are encouraged to follow it. New wind fields start with Flow at 1.
- **Noise Amount** and **Seed**: random variation in strength; the seed changes the pattern. Useful for natural gusts on flags and hair.
- **Shape**: Point, Line, Plane; mesh objects add Surface and Every Point.
- **Affect Location / Rotation**; **Absorption** (force is absorbed by collision objects); **Wind Factor** (how much the force is reduced when acting parallel to a surface such as cloth; 1 uses only the normal component).
- **Falloff**: Sphere, Tube or Cone with Power and Min/Max distance (see force-field-falloff).

## Gust animation

Keyframe Strength with a Noise F-curve modifier, or add a second wind with high Noise and low strength.

## Gotchas

- The simulation's Field Weights > Wind must be non-zero, and the field must be in its Effector Collection if one is set.
- Soft bodies react only to Force, Wind and Vortex fields.

## Verify

A flag ripples irregularly with Noise Amount above 0; with no noise the push is stiff and uniform.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/forces/force_fields/introduction and types/wind; branch blender-v5.2-release) and the 5.2 source (effect.cc, properties_physics_common.py). Confirmed: Add > Force Field menu, Wind direction along local Z, Strength and Flow semantics, Noise Amount, Seed, Affect options, Absorption, Wind Factor, Shape and Falloff options (manual); Plane shape and Flow 1 defaults for Wind (effect.cc); Noise Amount label (properties_physics_common.py).

Method: documentation only; no commands were run.
