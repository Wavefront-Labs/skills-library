---
id: creative-arts.animation.blender.floor-shrinkwrap-constraint
name: floor-shrinkwrap-constraint
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, floor-constraint, shrinkwrap-constraint, ground-contact, surface-snapping, rigging]
level: practitioner
status: docs-checked
description: "Keep feet, props and controls on surfaces with Blender's Floor constraint (offset, use rotation, min/max axis) and Shrinkwrap constraint (modes, snap mode, align to normal)."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/relationship/floor.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/relationship/shrinkwrap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# floor-shrinkwrap-constraint

## Floor

- The target object or bone defines the location, and optionally the rotation, of a virtual floor. **Min/Max** is the axis perpendicular to the floor pointing towards the walkable area: Z makes a floor, X or Y a wall, -Z a ceiling (global axes by default). **Offset** moves the floor up or down, for example to leave room for the actual foot. **Use Rotation** takes the Min/Max axes from the target's local axes instead of the global ones, so a rotated target gives a sloped floor.
- Use on IK foot controls so animators cannot push feet through the ground; or a "floor" for hand IK on a table.
- It is a planar limit only; uneven terrain needs Shrinkwrap.

## Shrinkwrap constraint

- Target: a mesh object. **Mode**: *Nearest Surface Point*, *Project* (along an axis; settings: Project Axis, Space, Distance cutoff where 0 is no limit, Project Opposite, Face Cull Off/Front/Back and Invert Cull), *Nearest Vertex*, *Target Normal Project* (better than Nearest Surface Point but slower).
- **Distance** is how far to stay away; **Snap Mode** decides how it is applied: On Surface, Outside Surface, Above Surface (offset along the interpolated normal), Inside, Outside. Inside and Outside only check the closest face, so they are crude collision and fail near sharp corners. Snap Mode is not available in Nearest Vertex mode.
- **Align To Normal** with an axis: rotates the owner (a swing rotation) to the interpolated surface normal; not available for Nearest Vertex.
- If Project finds no intersection the owner's location is left unchanged.
- Combine: Shrinkwrap Project on a foot control with Influence animated (on during contact, off in swing).

## Recipes

- **Character walking on uneven terrain**: foot IK control → child helper with Shrinkwrap Project with Project Axis -Z + Align To Normal; animators key the parent; helper follows terrain.
- **Eye highlights/decals sliding on a surface**: Shrinkwrap Nearest Surface + Align to Normal.

## Gotchas

- Target Normal Project uses interpolated vertex normals, which may not match the expected normal on flat-shaded meshes.
- Constraint order: the stack runs top to bottom, so put Shrinkwrap after Copy or Child Of constraints so it snaps the final position.

## Verify

Scrub: foot never penetrates ground; on slopes the control tilts with the surface when Align to Normal is used.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Floor and Shrinkwrap constraint pages: Min/Max axis, Offset, Use Rotation, Mode list, Project settings, Snap Mode list, Align To Normal limits. Removed the unconfirmed "Nearest Surface jumps on concave targets", high-poly performance and legacy Negative/Positive/Cull Faces wording; the Min/Max default is stated as global axes per the manual.

Method: documentation only; no commands were run.
