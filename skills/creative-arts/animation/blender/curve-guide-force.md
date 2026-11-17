---
id: creative-arts.animation.blender.curve-guide-force
name: curve-guide-force
category: creative-arts
field: animation
product: blender
tags: [blender, force-fields, curve-guide-force, curve-guide, drag-field, texture-field]
level: practitioner
status: docs-checked
description: "Steer Blender particles along paths with Curve Guide fields (clumping, free, min distance), the Texture field, and slow them with Drag fields."
sources:
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/curve_guide.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/drag.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/texture.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# curve-guide-force

## Curve Guide

1. Draw a curve object (only curve objects can carry a Curve Guide field). Physics > Force Field > Curve Guide.
2. Particles follow the guide during their lifetime; their speed along it depends on their lifetime and the length of the path.
3. Options: **Free** (fraction of particle lifetime not used for the curve), **Falloff Power** (strength between Min and Max Distance; 1 is linear), **Additive** (particle speed is also evaluated by falloff), **Weights** (curve weights influence particles along the curve), **Min Distance** (full strength up to this distance from the curve), **Max Distance** (maximum influence radius).
4. **Clumping Amount**: particles come together at the end of the curve (1) or drift apart (-1). **Shape**: +0.99 meets at the end, 0 is linear, -0.99 meets at the beginning.
5. To point particles along the curve, set their Orientation Axis to Velocity / Hair, enable Dynamic, and set Angular Velocity Axis to Velocity in the particle Rotation settings; the Follow Path constraint and the curve's legacy Follow option do not work for this.

## Kink

The Kink types (Curl, Radial, Roll, Wave, Braid, Rotation) have Axis, Frequency, Shape and Amplitude. The manual states this feature is broken in the current version (bug report 46776), so do not rely on it.

## Drag

Resists particle motion by slowing it down. **Linear** is proportional to velocity, **Quadratic** to its square.

## Texture field

Derives forces from a texture's colour: red = X, green = Y, blue = Z; 0.5 means no force. **Texture Mode**: Curl, Gradient or RGB (RGB needs a colour texture).

## Gotchas

- Several guides add up; limit their reach with Min Distance and Max Distance.
- The Curve Guide does not affect soft bodies.
- Guide timing is tied to particle lifetime, not distance.

## Verify

Particles emitted at the start follow the curve to its end over their lifetime.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/forces/force_fields/types/curve_guide, drag and texture; branch blender-v5.2-release) and the 5.2 source (properties_physics_field.py). Confirmed: Curve-only restriction, lifetime-based travel, Free, Falloff Power, Additive, Weights, Min/Max Distance, Clumping Amount and Shape ranges, orientation settings, the manual warning that Kink is broken, Drag Linear/Quadratic, Texture field colour coding and modes.

Method: documentation only; no commands were run.
