---
id: creative-arts.animation.blender.gn-math-utilities
name: gn-math-utilities
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-math-utilities, map-range, vector-math-node, float-curve, random-value, rotation-nodes]
level: practitioner
status: verified
description: "Use Geometry Nodes math utilities: Math/Vector Math ops, Map Range (linear, stepped, smoothstep), Float Curve, Random Value with ID/seed, Compare, Mix, and rotation sockets."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/math/index.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/math/map_range.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/random_value.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-math-utilities

Goal: the arithmetic layer of every GN tree — shaping ranges, randomness, vectors and rotations without hacks.

## Must-know nodes

- **Math**: Add, Multiply, Power, Truncated and Floored Modulo, Ping-Pong (bounces between 0 and *Scale*), Snap (floors to a multiple of *Increment*), Smooth Minimum/Maximum (blend width from *Distance*), Wrap (*Min*/*Max*), Compare (within *Epsilon*). *Clamp* limits the output to 0..1.
- **Vector Math**: Dot Product (facing ratio), Cross Product, Normalize, Length, Distance, Project, Reflect, Scale.
- **Map Range**: Float or Vector; *Linear*, *Stepped Linear* (quantises by *Steps*), *Smooth Step*, *Smoother Step*; *Clamp* limits the output to the target range.
- **Float Curve**: hand-drawn remap — tapers along Spline Parameter, falloffs.
- **Random Value**: Float/Integer/Vector/Boolean (Boolean uses *Probability*); **ID** (default: the `id` attribute if it exists, otherwise the index) and **Seed**. Connect a single value to ID for one random value for all elements. Values are not guaranteed unique.
- **Compare**: operations such as Less Than, Equal and Not Equal (within *Epsilon*); for vectors the *Mode* is Element-Wise, Length, Average, Dot Product (with input *C*) or Direction (with an *Angle* input).
- **Mix**: blends generic data types with a factor; **Switch** picks by a boolean.
- **Rotation nodes**: Euler to Rotation, Axis Angle to Rotation, Align Rotation to Vector, Rotate Rotation, Rotate Vector, Invert Rotation, Mix Rotation. The older Rotate Euler and Align Euler to Vector nodes are listed as deprecated.
- **Integer Math** for exact integer operations (Divide Round, Divide Floor, Divide Ceiling and others).

## Patterns

- Random per instance, stable over time: Distribute Points on Faces writes a stable `id` attribute that stays consistent when density or the mesh changes, and Random Value uses it by default.
- Facing ratio: Dot(Normal, Normalize(Camera position - Position)).
- Animated stagger: Map Range (Smooth Step) of Scene Time Seconds minus Index × delay.

## Gotchas

- Division by zero results in zero in the Math node, so such bugs are silent.
- Prefer rotation nodes over manual Euler maths.

## Verify

Viewer node on intermediate values; Spreadsheet shows values in range; change Seed to confirm randomness responds.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Math, Vector Math, Map Range, Compare, Integer Math, Random Value, Distribute Points on Faces, Menu/Scene Time pages: operation names, Map Range interpolation types, Random Value ID default, Compare modes, division by zero. Removed unconfirmed version gates, string comparison, and the Map Range equal-bounds claim.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Math operations Ping-Pong, Snap, Wrap, Smooth Minimum and Maximum, Compare, Truncated Modulo and Floored Modulo exist; 1 divided by 0 gave 0; Map Range types Linear, Stepped Linear, Smooth Step, Smoother Step; Compare vector modes Element-Wise, Length, Average, Dot Product (with input C) and Direction (with Angle); Integer Math Divide Round, Divide Floor, Divide Ceiling; Random Value Float, Integer, Vector with Min, Max, ID, Seed and Boolean with Probability; the rotation nodes, the older Rotate Euler and Align Euler to Vector nodes, Mix and Switch exist. Not run (confirmed from the manual only): the deprecation labels, ID defaulting to the id attribute, the three patterns.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
