---
id: creative-arts.animation.blender.deform-modifiers
name: deform-modifiers
category: creative-arts
field: animation
product: blender
tags: [blender, deform-modifiers, shrinkwrap, simple-deform, surface-deform, curve-modifier, mesh-deform]
level: advanced
status: docs-checked
description: "Blender Shrinkwrap, Simple Deform, Curve, Surface Deform and Mesh Deform modifiers: wrap methods and snap modes, deform axes and limits, binding rules, and known limits."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/shrinkwrap.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/simple_deform.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/surface_deform.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/mesh_deform.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/curve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# deform-modifiers

Goal: pick the right non-destructive deformer for the job and set it up so it behaves.

## Shrinkwrap

Moves each vertex of the modified object to the closest position on the surface of a *Target*. Works on meshes, lattices, curves, surfaces and texts.
- **Wrap Method:** *Nearest Surface Point*; *Project* (along chosen local axes until the target is hit; vertices that never hit stay put; options *Limit*, *Subdivision Levels* (temporary Catmull-Clark before wrapping), *Axis* (combinable; none selected uses the normal direction), *Negative/Positive*, *Face Cull*, *Invert Cull*, *Auxiliary Target*); *Nearest Vertex* (no extra options, and it does not support Snap Mode); *Target Normal Project* (similar to Nearest Surface Point, much smoother, significantly slower).
- **Snap Mode** (most methods): *On Surface* (vertex always moved; offset along the projection line), *Outside Surface* (offset always towards the target's outside), *Above Surface* (offset along the target's smooth normal), *Inside* (vertex not moved if already inside), *Outside* (not moved if already outside). Inside and Outside can serve as very crude collision detection but are not always stable near 90 degree and sharper target angles.
- *Offset* is the distance kept from the calculated target position. *Vertex Group*: vertices outside the group are not displaced.
- Gotcha: Project mode needs a sensible axis choice; with no axis selected it projects along the normal.

## Simple Deform

Twist and Bend rotate (set by *Angle*); Taper and Stretch scale (set by *Factor*); negative values reverse the deformation. Calculated in the object's local space along a *Deform Axis* (X, Y or Z), measured from the object's origin. *Limits* restrict the effect to part of the axis (the upper limit cannot be lower than the lower). An *Axis, Origin* object (usually an empty) can define the origin and axis: rotate it to change the axis, move it to move the origin, scale it to change the factor. *Lock* (Twist, Taper, Stretch only) controls whether coordinates along the other two axes can change. *Vertex Group* sets per-vertex influence.
- Bend is the least intuitive: the deform axis and the bending axis are paired (X with Z, Y with Z, Z with X), so a flat plane with Deform axis X or Y shows no deformation because every vertex shares the bending-axis coordinate.
- Twist: vertices in the plane of the origin are not rotated; those furthest from the origin rotate most.

## Curve

Deforms a mesh along a *Curve Object* using a dominant *Deformation Axis* (X/Y/Z/-X/-Y/-Z; default direction of travel is X): moving the mesh along that axis slides it along the curve like a train on rails, and moving it perpendicular changes its distance from the curve. Beyond the curve's ends the object keeps deforming along the end direction vectors. The modifier works in global space, so the geometry's position relative to the curve matters: set the object's origin to the geometry centre and start with it at the same location as the curve's origin. On a 3D curve, control-point *Tilt* twists the object and *Radius* sizes it (Shape panel, Path/Curve-Deform). *Vertex Group* and *Invert* are available.

## Surface Deform

Lets one mesh surface control another (for example a low-res cloth-simulation proxy driving a detailed mesh). *Target*, *Interpolation Falloff* (how much surrounding target faces affect a bound vertex; lower is smoother but may add slight artifacts; unavailable after binding), *Strength*, *Vertex Group* with *Invert*, *Sparse Bind* (records bind data only for vertices with nonzero weight at bind time; adding vertices to the group later needs a rebind), **Bind** / **Unbind**. Until bound the modifier has no effect.
- The target mesh must not contain edges with more than two faces, concave faces, overlapping vertices (doubles) or faces with collinear edges, or binding fails; the modified mesh has no restrictions.
- Binding uses global coordinates but later object transforms are ignored: the modified mesh only picks up changes to the target's mesh. The further the meshes deviate in shape, the more artifacts to expect.

## Mesh Deform

A closed mesh of any shape acts as a cage around another mesh. *Object* (the cage), *Vertex Group* with *Invert*, *Precision* (higher is more accurate but binding takes much longer; unavailable once bound), *Dynamic* (takes other modifiers and shape keys into account when binding; off by default; unavailable once bound), **Bind** / **Unbind**.
- Binding can be very slow, can leave Blender unresponsive and can run out of memory: save the blend-file first.
- Unbind resets the deformed object but not the cage.
- Cage normals must point outwards (they define inside and outside). Extra loose faces or smaller cages inside the main cage give extra control, for example around the eyes.
- Significant changes to the whole cage (such as flipping it upside down) can cause artifacts; a higher Precision reduces but does not remove them.

## Verify

- Playback: the deformed mesh follows the target or cage through the whole frame range with no popping.
- The modifier panel shows Bind (not Unbind) before binding, and Unbind afterwards.
- Surface Deform binding succeeds only after fixing target doubles, concave faces and edges with more than two faces.

## Checked

2026-10-28. Confirmed against the Blender manual pages for the Shrinkwrap, Simple Deform, Curve, Surface Deform and Mesh Deform modifiers: wrap methods and their options, snap modes, Simple Deform modes, limits, lock and the bend-axis pairing, the Curve modifier's global-space behaviour and origin advice, target-mesh validity rules, Sparse Bind, Precision and Dynamic, bind warnings and cage hints. Removed because the pages do not support them: the stack-order rules, default values and numeric ranges, Hook, Laplacian Deform, Smooth, Displace, Warp, Wave and Cast sections, shape-key baking and export advice, and the sample offsets and settings.
Method: documentation only; no commands were run.
