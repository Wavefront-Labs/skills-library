---
id: creative-arts.animation.blender.rigid-body-shapes-mass
name: rigid-body-shapes-mass
category: creative-arts
field: animation
product: blender
tags: [blender, rigid-body, rigid-body-collision-shapes, convex-hull, compound-shape, rigid-body-mass-friction, calculate-mass, bounciness, collision-margin]
level: practitioner
status: docs-checked
description: "Choose Blender rigid body collision shapes (primitives, convex hull, mesh, compound parent) and set mass, Calculate Mass, friction, bounciness and margins."
sources:
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/properties/collisions.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/properties/settings.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/rigid_body.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# rigid-body-shapes-mass

## Collision shapes (Physics > Rigid Body > Collisions > Shape)

- **Primitive shapes** (**Box**, **Sphere**, **Capsule**, **Cylinder**, **Cone**): best in memory and performance but may not match the real shape. Size comes from the object's bounding box and the centre of gravity is the shape's geometric centre. Show them with the Extras overlay. Capsule, Cylinder and Cone point up the Z axis; Sphere radius is the largest bounding-box axis; Box also covers planes such as ground.
- **Convex Hull**: a convex approximation wrapped over all vertices, with good performance and stability (best with fewer vertices). The centre of gravity is the object origin.
- **Mesh**: triangles only; allows concave objects and detailed interaction but is rather slow and unstable.
- **Compound Parent**: takes the collision shapes from the object's children and combines them, giving concave shapes from primitives; usually faster and more stable than Mesh.
- **Source** (mesh shapes): **Base**, **Deform** (shape keys and deform modifiers) or **Final** (all modifiers). **Deforming** lets mesh shapes deform during the sim.
- **Margin** (Sensitivity): distance threshold near the surface where collisions are still considered; best results when nonzero. The margin is embedded for Sphere, Box, Capsule, Cylinder and Convex Hull, but not for Cone and Triangle Mesh, which show a gap; Passive Triangle Mesh can usually be set to 0.

## Mass and surface (Physics > Rigid Body > Settings and Collisions)

- **Mass**: how heavy the object is, irrespective of gravity.
- **Object > Rigid Body > Calculate Mass**: computes mass from volume and density. **Material Preset** lists densities for real-world materials; choose Custom and enter **Density** in kg per cubic metre otherwise.
- **Friction**: resistance to movement; how much velocity is lost when objects collide.
- **Bounciness**: tendency to bounce after colliding, from 0 (rigid) to 1 (perfectly elastic).
- **Collections**: rigid body collisions can be allocated to different groups (maximum 20).

## Gotchas

- Small objects are unstable; the manual says objects should ideally be at least 20 cm in diameter, and setting the margin to 0 can help small ones (not generally recommended).
- Fast or small objects can pass through each other; avoid Mesh shapes, since triangles have no thickness, and raise the margin to give thickness.
- A high-poly Convex Hull is best avoided; use a simpler proxy.
- Apply scale (Ctrl+A) if you do not need dynamic scaling.

## Verify

Show collision shapes with the Extras overlay; objects rest on surfaces without visible gaps.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: shape list and descriptions, Source options, margin embedding table, Calculate Mass and Material Preset, Friction, Bounciness (0 to 1) and the 20-collection maximum, and the small-object and fast-object guidance. Corrected the margin default (0.04 m, not in the manual) and the scale-up-the-scene tip; removed "combined from both bodies" for friction and the requirement that compound children carry their own rigid body.
Method: documentation only; no commands were run.
