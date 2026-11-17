---
id: creative-arts.animation.blender.curve-tilt-radius
name: curve-tilt-radius
category: creative-arts
field: animation
product: blender
tags: [blender, curve-object, curve-tilt, curve-radius, tilt, twist-method, roller-coaster, curve-modeling]
level: practitioner
status: docs-checked
description: "Set per-point tilt (Ctrl T) and radius (Alt S) on Blender curves: Clear Tilt, Smooth Curve Tilt/Radius, Bezier tilt interpolation and how they drive bevels and twist."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/curves/editing/control_points.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/editing/curve.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/properties/active_spline.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/properties/shape.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# curve-tilt-radius

Goal: control banking (rails, ribbons) and per-point thickness without extra objects.

## Tilt

- Edit mode, select points, `Ctrl T` (Tilt tool, Control Points > Tilt). Tilt controls how the normals (shown as arrows) twist around each control point, so it is only relevant with 3D curves. The Sidebar Transform panel also has a **Tilt** field.
- **Clear Tilt**: `Alt T` resets tilt to its default (perpendicular to the original curve plane).
- Tilt is interpolated from point to point; check it with the normals overlay (Curve Edit Mode Overlays > Normals).
- NURBS tilt is always smoothly interpolated. For Bezier splines, Active Spline > **Interpolation Tilt** picks the algorithm (Linear, Cardinal, BSpline, Ease).
- **Smooth Curve Tilt** (Control Points menu) interpolates tilt over the selected points to reduce sharp changes.
- Tilt and radius also change the direction and distance of the Geometry panel Offset and Extrude.

## Radius

- `Alt S` (Radius tool, Curve > Transform > Radius) sets the width of the extrusion/bevel along the curve; the Sidebar Transform panel has a **Radius** field. It is interpolated from point to point.
- Active Spline (Bezier) > **Radius** picks how the radius of a beveled curve is interpolated.
- **Smooth Curve Radius** (Control Points menu) smooths radius changes over the selected points.
- Curve Deform > **Radius** (Shape panel) scales an object deformed along the curve by the curve radius (curve used as a path or with the Curve modifier).
- Combine with Taper Radius mode Multiply (see curve-taper).

## Twist Method (Shape panel)

*Minimum*, *Tangent* or *Z-Up* decide how the twist of a 3D curve is calculated; tilt is applied on top. **Smooth** removes kinks from over-twisting.

## Gotchas

- Radius 0 on a control point collapses the bevel there (the manual's radius figure shows one point set to zero).
- Big tilt changes between few points twist the geometry; add points or use Smooth Curve Tilt.

## Verify

With Normals shown, the arrows rotate as intended along the spline; clear with `Alt T` and the arrows return to the default orientation.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Control Points, Curve editing, Active Spline and Shape pages, curve display overlays) and 5.2 source enum for tilt interpolation. Confirmed: Ctrl T, Alt T, Alt S, Transform panel Tilt/Radius fields, tilt interpolation options for Bezier, smoothing operators, Twist Method options, Curve Deform Radius. Removed as unconfirmed: Follow Path banking and Curve Radius constraint claims, Geometry Nodes attribute names and the "towel" twist advice beyond adding points.
Method: documentation only; no commands were run.
