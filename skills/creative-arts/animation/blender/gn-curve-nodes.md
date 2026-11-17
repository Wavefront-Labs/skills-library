---
id: creative-arts.animation.blender.gn-curve-nodes
name: gn-curve-nodes
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-curve-nodes, curve-to-mesh, resample-curve, trim-curve, curve-parameter, cables]
level: practitioner
status: verified
description: "Build cables, pipes and vines with Geometry Nodes curve nodes: Curve to Mesh with profile and scale, Resample, Trim, Spline Parameter, Set Curve Radius/Tilt, Curve to Points."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/index.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/operations/curve_to_mesh.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/curve/operations/resample_curve.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-curve-nodes

Goal: procedural tube/sweep geometry from curves with control over taper, density and growth animation.

## Core chain

`Curve (object/primitive) → Resample Curve → Set Curve Radius → Curve to Mesh (Profile = Curve Circle) → Set Material`

- **Curve to Mesh**: *Profile Curve* (Curve Circle, Quadrilateral, or any curve; no profile gives a chain of edges), **Scale** (scales the profile at each point), **Fill Caps** (n-gon caps when the profile spline is cyclic). (The 4.5.14 node has only Curve, Profile Curve, Scale and Fill Caps; the Miter Scale and Limit inputs of the 5.x manual do not exist there.)
- **Resample Curve**: *Count* or *Length* mode give uniform spacing on new poly splines (Length is rounded down to whole samples); *Evaluated* uses the resolution attribute.
- **Spline Parameter**: Factor (portion of spline length at each control point), Length, Index. It reads values at control points, so resample first on Bezier or NURBS curves. Taper with Radius = Float Curve(Factor).
- **Trim Curve**: *Factor* or *Length* mode with *Start* and *End*; animate End from 0 to 1 for growing vines. A cyclic spline is trimmed too (4.5.14: a 32-point Curve Circle with End 0.5 came out with 18 points).
- **Set Curve Tilt** twists profiles; also **Set Handle Type**, **Fillet Curve** and **Subdivide Curve**.
- **Curve to Points** (*Evaluated*, *Count* or *Length* mode) outputs Tangent, Normal and Rotation; use with Instance on Points for chain links or fence posts.

## Recipes

- **Hanging cable between two empties**: Curve Line (Start/End from Object Info locations) → Resample 32 → Set Position Offset Z = -(sag × 4 × f × (1-f)) where f = Spline Parameter Factor → Curve to Mesh with Curve Circle radius 0.02.
- **Growing vine**: Trim Curve End = animated 0→1, Radius = Float Curve(Factor) tapering to 0 at the tip.

## Gotchas

- Set Curve Radius controls the profile size used by Curve to Mesh; Scale multiplies it further.
- Trim Curve turns NURBS splines into poly splines.
- For UVs along the tube, store Spline Parameter Length and a profile coordinate in a 2D vector attribute with Store Named Attribute.

## Verify

Viewer node on the curve with Spline Parameter Factor shows a gradient from 0 to 1; scrubbing Trim End grows the mesh.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Curve to Mesh, Resample Curve, Spline Parameter, Trim Curve, Curve to Points and Set Curve Radius pages: socket and mode names, Trim limitations, Spline Parameter caveat. Removed unconfirmed version gate and the claim that profile and curve radius multiply.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Resample Curve in Count mode gave 10 points and in Length mode 0.3 on a length-1 line gave 4 points (rounded down to whole samples); Curve to Mesh with an 8-point circle profile on 4 points gave 32 vertices and 24 faces, 26 faces with Fill Caps, and with no profile 4 vertices and 3 edges; Curve to Points modes Evaluated, Count, Length with Tangent, Normal and Rotation outputs; Spline Parameter outputs Factor, Length, Index; Set Curve Radius, Set Curve Tilt, Fillet Curve, Subdivide Curve exist. Wrong in the old text: Trim Curve does handle a cyclic circle, and the Miter Scale and Limit inputs are not on the 4.5.14 node. Not run (confirmed from the manual only): NURBS-to-poly conversion, the cable and vine recipes, UV attribute recipe.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
