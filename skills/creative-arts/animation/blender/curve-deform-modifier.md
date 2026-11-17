---
id: creative-arts.animation.blender.curve-deform-modifier
name: curve-deform-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, curve-modifier, curve-deform, modifiers, deform, path, stretch, bounds-clamp]
level: practitioner
status: verified
description: "Set up Blender's Curve modifier: global-space origin alignment, deformation axis, Stretch/Bounds Clamp, curve radius and tilt, twist method, and Array combos."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/curve.html
  - https://docs.blender.org/manual/en/latest/modeling/curves/properties/shape.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# curve-deform-modifier

Goal: make a mesh follow a curve (cables, roads, snakes, chains) and move along it, without the "mesh jumps away" failure.

## How it works

The modifier deforms along a dominant axis (X by default; X, Y, Z, -X, -Y, -Z are offered). Moving the mesh along that axis makes it traverse the curve like a train on rails; moving it perpendicular moves it closer to or further from the curve. Beyond the curve's ends the object keeps deforming along the direction vector at the end.

The modifier works in **global space**: the real position of the geometry relative to the curve decides the result.

## Setup

1. Put the mesh's origin at the centre of its geometry (Set Origin to Geometry) and start with the mesh origin at the same location as the curve object's origin (snap tools).
2. Add the *Curve* modifier. Set *Curve Object* and *Deformation Axis* (the axis the mesh is long in, in global space).
3. Move the mesh along that axis to slide it along the curve; keyframe that location for travel animation.
4. *Vertex Group* (+ Invert) restricts the effect.

## Curve-side options (Curve Object Data, Shape panel, Curve Deform)

- **Radius**: scales the deformed object by the curve's point radius (also used for paths).
- **Stretch**: stretches or squeezes the mesh over the whole curve; the manual says to use it together with **Bounds Clamp**.
- **Bounds Clamp**: ignores the object and mesh offset along the deformation axis (useful with Stretch or a negative axis).
- **Tilt** of control points in a 3D curve twists the deformed object.
- **Twist Method**: *Minimum*, *Tangent* or *Z-Up*; **Smooth** removes kinks from over-twisting.
- **Resolution Preview U**: points computed between control points; low values look faceted.

## Combining with Array

A repeated segment can be placed before the Curve modifier in the stack so it is deformed after being repeated. The legacy Array modifier (named *Array (Legacy)* in the Blender 5.2 manual) has a *Fit Curve* fit type that fills the length of a curve object. The manual's tentacle example uses an Array followed by a Curve modifier.

## Gotchas

- Origins not aligned: the mesh appears displaced; fix origins before blaming the axis.
- Deformation Axis must be the mesh's long axis.
- Apply object rotation and scale if results look off, because the modifier is evaluated in global space.

## Verify

Moving the mesh along the deformation axis slides it along the curve with no sideways drift; with Stretch and Bounds Clamp the mesh spans the whole curve.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Curve modifier, curve Shape pages, Array (Legacy) page). Confirmed: global-space behaviour, axis options, Radius, Stretch, Bounds Clamp, Twist Method, Smooth, Resolution Preview U, Fit Curve. Corrected the earlier local-space claim. Removed unconfirmed shortcuts, spline-count and resolution figures.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Curve modifier with Python on a 20-column grid and a three-point curve (8 units long, bending 90 degrees): Deformation Axis has X, Y, Z, -X, -Y, -Z (default X); moving the object or shifting the geometry by 2 along X slid it along the curve (the same world result), i.e. evaluation is in global space; moving the curve object by 1 in Y changed the result, and rotating the mesh object 90 degrees changed the result (the axis is taken in global space); an object placed at x=9 (mesh spanning 7 to 11 on an 8-unit curve) continued straight along the end direction (world y up to 7.0), and one at x=-3 extended straight back before the start; Stretch plus Bounds Clamp made the mesh span the curve; Radius on doubled the width; the curve properties are Radius (default on), Stretch, Bounds Clamp, Twist Method (Z-Up, Minimum default, Tangent), Twist Smooth and Resolution U (default 12). Not run: Tilt twisting, Array Fit Curve in the same stack (Fit Curve is covered in array-offsets), and the origin set-up steps.

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
