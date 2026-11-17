---
id: creative-arts.animation.blender.nurbs-weights-order
name: nurbs-weights-order
category: creative-arts
field: animation
product: blender
tags: [blender, nurbs, nurbs-weights, nurbs-order, nurbs-endpoint, active-spline, curve-object, surfaces]
level: practitioner
status: verified
description: "Shape NURBS curves in Blender: Order U, Endpoint and Bezier knot options, Cyclic, control point Weight (W) and Resolution; NURBS circle primitive."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/curves/properties/active_spline.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/structure.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/editing/transform_panel.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/primitives.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# nurbs-weights-order

Goal: smooth, mathematically exact curves driven by control-point weights instead of handles.

## Active Spline panel (Sidebar > Item > Active Spline, Edit mode, per spline)

- **Cyclic U**: closes the spline.
- **Bezier U**: makes the NURBS curve act like a Bezier curve; the NURBS control points act like Free handles.
- **Endpoint U**: makes the curve touch the end control points. Endpoint and Bezier only apply to open NURBS curves; they influence the (non-editable) knot vector.
- **Order U**: area of influence of the control points. Higher order means one point influences a greater part of the curve. Valid range is 2 to 6 depending on the number of control points (deleting points can lower it). Tested on a 5-point spline: `order_u` set to 1 gave 2, 6 and higher gave 5, so out-of-range values are clamped, not rejected.
- **Resolution U**: subdivisions per segment. **Smooth**: smooth shading for 3D geometry.

## Weights

- NURBS control points have a **W** (weight) field in the Sidebar Transform panel (median value when several points are selected).
- If all control points have the same weight their influences cancel out; differences in weight pull the curve toward or away from specific points.
- This is different from the *Goal Weight* used by soft body physics (the separate Weight field in the same panel).
- Bezier points have no W.

## Why NURBS

- NURBS can represent exact geometry (a NURBS circle is exact; a Bezier circle approximates).
- Add > Curve > **NURBS Circle** is a closed circle of eight control points (order 3); **NURBS Curve** is an open curve of four points with Uniform knots (order 4, Endpoint off); **Path** is an open curve of five points with Endpoint knots (order 5). The three primitive operators all gave `dimensions == '3D'` in 4.5.14.
- Smooth Curve Weight (Control Points menu) interpolates weight over selected points.

## Gotchas

- Set Spline Type (Bezier, NURBS, Poly, Catmull Rom) is a basic conversion: check shape and point count afterwards (a 4-point Bezier circle gave 4 NURBS points in 4.5.14).
- Without Endpoint the curve does not reach the first and last control points.

## Verify

Toggle Endpoint and watch the ends move to the first and last points; give one point a clearly different W and see the curve move toward or away from it.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Active Spline, Curve structure, Transform panel, Curve primitives, Curve editing). Confirmed: Active Spline fields for NURBS, Endpoint/Bezier scope, Order range 2-6, W field and weight behaviour, primitive point counts, Set Spline Type note. Corrected: Bezier U does not mean "passes through every Order-th point" (control points act like Free handles); the "order 2 = polyline, 3 = quadratic, 4 = cubic default" mapping and the NURBS surface (V) options were removed as unconfirmed here.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: `Spline` has `order_u`, `use_endpoint_u`, `use_bezier_u`, `use_cyclic_u`, `resolution_u`, `use_smooth`; defaults order 4 with Endpoint and Bezier off; Endpoint on made the curve reach the first and last control points (x from 0.99 to 3.01 became -0.01 to 4.01); a weight of 5 on one point pulled the curve toward it (max y 0.90 to 1.67) while equal weights (1 or 3) gave the same curve; NURBS points have a fourth `co` component and a separate `weight_softbody`, Bezier points have neither; primitive point counts, cyclic and Endpoint flags as written above; `spline_type_set` types POLY, BEZIER, NURBS; operators `smooth_weight`, `smooth_radius`, `smooth_tilt`, `switch_direction` exist. Unrun: Sidebar panel layout and labels, Bezier U behaviour beyond running it (documentation only).

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
