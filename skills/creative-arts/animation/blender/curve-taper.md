---
id: creative-arts.animation.blender.curve-taper
name: curve-taper
category: creative-arts
field: animation
product: blender
tags: [blender, curve-object, curve-taper, taper-object, taper-radius, horns, tails, curve-geometry]
level: practitioner
status: verified
description: "Vary thickness along Blender curves: Taper Object scale graph, Taper Radius mode (Override, Multiply, Add), Map Taper with Factor Start/End, versus per-point radius."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/curves/properties/geometry.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/editing/curve.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# curve-taper

Goal: horns, tentacles, tails, vines and brush strokes whose thickness changes along the length.

## Taper Object (Geometry panel)

- A separate Curve object made of a single, non-cyclic, 2D spline. It controls the scale factor of the geometry along the length of each spline of the main curve. The name is misleading: it can apply any size anywhere.
- It is a graph: the X axis is the position along the curve, the Y axis is the scale. Y = 1.0 leaves the geometry unchanged, 0.5 halves it, 2.0 doubles it. The X range does not matter ([-10, 10], [-1, 1] and so on).
- The first control point of the Taper Object corresponds to the first control point of each geometry spline, and the last to the last.
- The manual says the first Taper point should have the highest X coordinate and the last the lowest; if the scaling does not seem to work, use Segments > Switch Direction on the taper curve.
- The Z coordinates of the taper points are ignored; setting the taper object to Dimensions 2D forces them to 0.

## Taper Radius (how taper combines with per-point radius)

- **Override**: the taper replaces the radii of the control points.
- **Multiply**: taper scale multiplied by the point radius (taper for the global shape, radius for local bulges).
- **Add**: taper scale added to the point radius.
- Per-point radius is set with the Radius tool (`Alt S`, Edit mode) or the Radius field in the Sidebar Transform panel.

## Map Taper and Factor Start/End

- **Factor Start / End** (Start & End Mapping) limit the geometry to part of the curve (default 0 and 1); *Mapping Start/End* choose Resolution, Segments or Spline mapping.
- **Map Taper**: when geometry covers only part of the curve, the endpoints of the Taper Object correspond to the ends of the geometry instead of the ends of the curve, so the tip stays pointed while Factor End grows.

## Radius-only alternative

Skip the taper object: set Radius per control point. Fine for a few points, awkward for long smooth gradients.

## Verify

Animate Factor End from 0 to 1 with Map Taper on: the tip stays tapered during the growth.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (curve Geometry panel and Curve editing page). Confirmed: Taper Object definition and graph axes, Y scale values, Z ignored, Switch Direction hint, Taper Radius Override/Multiply/Add, Map Taper, Factor Start/End and Mapping, Alt S radius shortcut. Corrected: "Bevel Start/End" is named Factor Start/End, and "Y = 0 gives a point" was an extrapolation of the documented scale values (now stated as the documented 1.0, 0.5, 2.0 examples). Removed as unconfirmed: cap and render-visibility gotchas and the claim that taper scales Extrude.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: a taper curve with Y going from 1 to 0.5 halved the bevel radius at the end of the curve (0.1 to 0.05); `taper_radius_mode` items OVERRIDE, MULTIPLY, ADD behaved as described with point radius 2 and a taper of 0.5 (0.05, 0.1, 0.25 mid-curve radius); a per-point radius alone doubled the tube (0.2); `bevel_factor_start/end` default 0 and 1; `use_map_taper` on changed the end radius from 0.06 to 0.02 with Factor End 0.5; setting `dimensions = '2D'` set the Z of 3D points to 0. Unrun: taper graph axis and direction rules, Switch Direction hint, Alt S radius tool.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
