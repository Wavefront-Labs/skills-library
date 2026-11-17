---
id: creative-arts.animation.blender.shear-to-sphere-transforms
name: shear-to-sphere-transforms
category: creative-arts
field: animation
product: blender
tags: [blender, shear, to-sphere, push-pull, bend-transform, warp-transform, transform-tools, mesh-editing]
level: practitioner
status: docs-checked
description: "Use Blender's special transforms: Shear, To Sphere, Push/Pull, Bend, Warp, Shrink/Fatten — hotkeys, pivot/cursor dependence, and modelling uses like round holes and arches."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/transform/shear.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/transform/to_sphere.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/transform/bend.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/transform/warp.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/transform/push_pull.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/transform/to_circle.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/transform/shrink-fatten.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# shear-to-sphere-transforms

Goal: shape geometry with the less-known transforms in *Mesh > Transform* (most also work on objects).

## The tools

- **To Sphere** `Shift Alt S` (Object and Edit Modes): deforms the selection to look more like a sphere; move the mouse or type a Factor between 0 and 1. Denser meshes give better results. Options: Factor, Mirror Editing, Proportional Editing.
- **To Circle** (Mesh > Transform > To Circle, Edit Mode): transforms selected vertices into a circle; works best on edge loops. Options: Factor, Method (Best Fit or Interior Fit), Rotation, Radius, Space Evenly. This is the tool for making a round hole from a loop (practice).
- **Shear** `Shift Ctrl Alt S` (Object and Edit Mode, also a toolbar tool): moves vertices above the pivot point one way and below it the other, so vertical edges become diagonal. By default "above", "below" and "horizontal" are in the viewing plane; options: Angle, Axis (perpendicular to the shearing plane), Axis Ortho, Orientation.
- **Push/Pull** (Object/Mesh > Transform, no default key): moves the selection further from or closer to the pivot point, all by the same distance (Distance: negative pushes, positive pulls).
- **Bend** `Shift W`: bends part of the selection into a circle segment; the 3D Cursor lies on the circle. Align the view to the bend plane, put the 3D Cursor at the base of the bend, then move the mouse; the mouse distance from the cursor sets the radius, and `Alt` disables clamping. It has no redo panel.
- **Warp** (Edit Modes, no default key): like Bend, but the 3D Cursor is at the circle's centre. Options in the redo panel: Warp Angle, Offset Angle, Min/Max.
- **Shrink/Fatten** `Alt S` (Edit Mode): moves vertices inward or outward along their normals by the same distance; *Offset Even* offsets each edge, rather than each vertex, by the same distance (`S` or holding `Alt` toggles it).

## Gotchas

- Bend and Warp ignore the transform orientation and pivot point and always use the view plane and the 3D Cursor, so set both deliberately.
- Shear, Push/Pull and To Sphere depend on the pivot point.
- These are destructive edits; for animatable bends use the Simple Deform modifier (practice).

## Verify

The redo panel (where supported) shows exact values; Bend has no redo panel.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/meshes/editing/mesh/transform/ pages (to_sphere, to_circle, shear, push_pull, bend, warp, shrink-fatten): shortcuts, modes, options and cursor/pivot dependence. Wrong claims fixed: To Sphere is not the round-hole tool (To Circle is), Warp and Bend ignore pivot and orientation, Push/Pull is a uniform distance move. Removed the 8-vertex loop claim and the LoopTools claim.

Method: documentation only; no commands were run.
