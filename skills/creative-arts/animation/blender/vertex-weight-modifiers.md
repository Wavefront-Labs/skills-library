---
id: creative-arts.animation.blender.vertex-weight-modifiers
name: vertex-weight-modifiers
category: creative-arts
field: animation
product: blender
tags: [blender, weight-mix, weight-mix-modes, weight-proximity, weight-proximity-falloff, vertex-weight-edit, vertex-groups, procedural-weights, modifiers]
level: practitioner
status: docs-checked
description: "Build procedural vertex groups with Blender's Vertex Weight Proximity, Mix and Edit modifiers: distance mapping, Vertex Set, mix modes, falloff, thresholds, influence."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weight_proximity.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weight_mix.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weight_edit.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# vertex-weight-modifiers

Goal: weights computed live (distance to an object, combinations of groups) that drive other modifiers such as Wave or Displace.

All three modifiers clamp weights to 0.0 to 1.0, and Weight Paint Mode shows the modified weights, so disable the modifier to see the original group.

## Vertex Weight Proximity
- **Vertex Group**: the group to affect. **Target Object**: where distances are measured to.
- **Proximity Mode**: *Object* (distance between the two object origins; every affected vertex gets the same weight) or *Geometry* (distance from each vertex to the target's geometry).
- **Geometry** (in Geometry mode): Vertex, Edge, Face; with several enabled the shortest distance is used. A target without geometry (empty, camera) falls back to its origin.
- **Lowest / Highest**: distances mapped to weight 0.0 and 1.0; set Lowest above Highest to reverse. **Normalize Weights** rescales to the full 0 to 1 range.
- **Falloff** Type: Linear, Custom Curve, Sharp, Smooth, Root, Sphere, Random, Median Step (binary 0 or 1 at 0.5); Invert toggle.

## Vertex Weight Mix
- **Vertex Group A** (affected) and **B** (mixed in; leave empty to mix a simple value), each with Invert Weights, and **Default Weight A/B** for vertices not in the group.
- **Vertex Set**: All, Vertex Group A, Vertex Group B, Vertex Group A or B, Vertex Group A and B. With All, group B or one group, vertices might be added to the affected group.
- **Mix Mode**: Replace, Add, Subtract, Multiply, Divide, Difference, Average, Minimum, Maximum. **Normalize Weights** as above.

## Vertex Weight Edit
- **Vertex Group**, **Default Weight**, **Group Add** (adds vertices whose final weight is over *Add Threshold*), **Group Remove** (removes vertices below *Remove Threshold*), **Normalize Weights**.
- **Falloff** Type: Linear (no mapping), Custom Curve, Sharp, Smooth, Root, Sphere, Random, Median Step; Invert.

## Influence (shared by all three)
**Global Influence** (0.0 leaves weights untouched, 1.0 standard; it does not stop vertices being added or removed), plus an optional per-vertex vertex group or texture mask (mutually exclusive) multiplied with it.

## Examples from the manual
Proximity driving a Wave modifier through a modified group; Weight Edit with Proximity feeding a Displace modifier; Mix driven by a texture with a custom mapping curve.

## Gotchas
- With Vertex Set limited to a group that is empty, nothing changes.
- Modifier order matters: place the weight modifiers above the modifier that reads the group.

## Verify
Move the target object and watch the group in Weight Paint Mode (or the Spreadsheet in evaluated state).

## Checked
Date: 2026-10-27. Documentation: Blender manual, Vertex Weight Proximity, Mix and Edit modifier pages, branch blender-v5.2-release. Confirmed: all option names above, including Vertex Set (not Mix Set), Median Step (not Step), Group Add and Remove thresholds and shared Influence settings. Removed unconfirmed recipes (wetness, wrinkle mask), Attribute node shader read, "On Cage" visualisation and the exact modifier ordering chain.
Method: documentation only; no commands were run.
