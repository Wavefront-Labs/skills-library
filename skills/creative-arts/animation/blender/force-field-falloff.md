---
id: creative-arts.animation.blender.force-field-falloff
name: force-field-falloff
category: creative-arts
field: animation
product: blender
tags: [blender, force-fields, force-field-falloff, field-shape, max-distance]
level: practitioner
status: docs-checked
description: "Control where Blender force fields act: shape (point, line, plane, surface), falloff type, power, min/max distance and tube/cone settings."
sources:
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/introduction.html
  - https://docs.blender.org/manual/en/latest/physics/forces/force_fields/types/texture.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# force-field-falloff

## Shape (Settings)

Sets the direction used to calculate the force. Empties offer Point, Line and Plane; 3D objects add Surface and Every Point; curves add Curve.

- **Point**: omnidirectional, from the object origin.
- **Line**: the force acts only in the local XY plane, using the Z axis line as the effector.
- **Plane**: the force acts only in the local Z direction, using the XY plane as the effector.
- **Surface**: acts on a 3D object's surface; the Z axis is the surface normal.
- **Every Point**: every vertex of the mesh is an effector point.

## Falloff panel

- **Shape**: Sphere (uniform), Tube (adds Radial settings: Power, Use Minimum/Maximum, Min/Max Distance) or Cone (Angular settings: Power, Use Min/Max Angle).
- **Z Direction**: Both Z, +Z or -Z.
- **Power**: how the force changes with distance r: 1/(r - min + 1)^power. A power of 2 is similar to gravitational pull; 0 means full strength out to Max Distance.
- **Min Distance**: distance from the origin up to which the field has full strength (no effect when Power is 0). **Max Distance**: maximum radius of influence. Both are shown as circles around the object.

## Practice

- Use Max Distance on local effects so they do not touch the whole scene; fields affect everything by default.
- A Texture field with a procedural texture gives spatially varying forces.
- Strength scales with the force object's scale, so scaling the scene keeps the same effect.

## Verify

Place a test particle stream: particles beyond Max Distance are unaffected, and with Power 0 the force is constant up to the limit.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/forces/force_fields/introduction (Shape, Falloff) and types/texture; branch blender-v5.2-release) and the 5.2 source (properties_physics_field.py). Confirmed: Shape options and which object types offer them, Falloff Shape, Z Direction, Power formula, Min/Max Distance and circle display, strength scaling; Tube Radial and Cone Angular sub-panels (properties_physics_field.py).

Method: documentation only; no commands were run.
