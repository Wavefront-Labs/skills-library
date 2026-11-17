---
id: computing-software.computer-graphics-engineering.graphics-math.curves-and-splines-for-graphics
name: curves-and-splines-for-graphics
category: computing-software
field: computer-graphics-engineering
product: graphics-math
tags: [graphics-math, bezier, spline, catmull-rom, hermite, nurbs, bspline, camera-path, arc-length-parameterization, de-casteljau, tessellation, curve-fitting, path-animation]
level: advanced
status: draft
description: "Bezier/Catmull-Rom/Hermite/B-spline curves for camera paths and curve tools: continuity (C0/C1/C2), arc-length reparameterization, de Casteljau evaluation, and tessellation."
sources: ["https://pomax.github.io/bezierinfo/", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Curves and splines for graphics

**Goal:** pick the right curve type for the job (camera paths, cable/rope shapes,
curve-based tools) and evaluate/sample it without the classic bugs — uneven speed
along the curve, wrong continuity at joins, or a tessellation that's too coarse or
wastefully fine.

## Curve types and when to use which
- **Bezier** (cubic, 4 control points): intuitive artist handles (2 endpoints + 2
  tangent-defining control points), but a chain of independent Bezier segments is
  only **C0 continuous** (positions match) at joins unless you manually align
  tangent handles — the standard vector-tool authoring curve (Illustrator/Photoshop
  pen tool, Blender Bezier curves).
- **Catmull-Rom / Hermite**: interpolates *through* a given set of points (no
  separate control points to place) with automatically **C1 continuous** tangents
  computed from neighbouring points — the standard choice for camera paths and
  motion paths through specified waypoints, since you usually have waypoints, not
  hand-placed tangent handles.
- **B-spline / NURBS**: control points **don't** lie on the curve (approximating,
  not interpolating) — gives C2 continuity (smooth curvature, no visible kinks in
  the derivative) and is the standard for CAD/surface modelling where curvature
  continuity matters more than passing exactly through points.
- Continuity matters concretely: C1 breaks show as a visible kink in camera
  *velocity* (a sudden speed/direction change) even if position is continuous; C2
  breaks show as a kink in *acceleration*, subtler but still visible as a flicker
  in smooth dolly/crane shots.

## Evaluation
- **De Casteljau's algorithm**: evaluate a Bezier point at parameter `t` by
  repeated linear interpolation between control points — numerically stable
  (unlike expanding the Bernstein polynomial directly), and the standard method
  for both evaluation and subdivision (splitting a curve into two Beziers at `t`).
- Catmull-Rom segment between P1,P2 given neighbours P0,P3: standard matrix form
  with tangents `(P2-P0)/2` and `(P3-P1)/2` — note the **uniform** parameterization
  can overshoot/loop on unevenly spaced points; **centripetal Catmull-Rom**
  (tangents scaled by distance^0.5 between points) fixes cusps/loops on non-uniform
  waypoint spacing and is the version to default to for authored waypoints.

## Arc-length reparameterization
A curve's parameter `t` does **not** correspond to constant speed along its
length — points bunch up where the curve is "slow" in `t` and spread out where
it's "fast." For a camera dolly or any motion that must move at constant (or
deliberately eased) speed:
- Precompute an **arc-length table**: sample the curve densely, accumulate
  segment lengths, build a `t → arc-length` lookup.
- To move at constant speed, invert the table: given a desired arc-length
  (`speed * elapsedTime`), binary-search/interpolate the table for the
  corresponding `t`, then evaluate the curve at that `t`.
- Skipping this step is the single most common curve-animation bug: motion that
  "speeds up" through tightly-spaced control points and "slows down" through
  widely-spaced ones, even though the artist intended constant speed.

## Tessellation
- Flatten to line segments for rendering/collision at a tolerance relative to
  screen-space or world-space error (recursive subdivision: split until the
  midpoint deviates from the chord by less than a pixel threshold), not a fixed
  segment count — a fixed count either over-tessellates gentle curves or
  under-tessellates sharp ones.

## Verify
- [ ] Continuity at segment joins matches the visual requirement (C1 minimum for
      camera paths) — check by plotting velocity, not just position.
- [ ] Constant-speed motion verified via arc-length reparameterization, not raw
      `t`-parameter stepping, whenever waypoint spacing is uneven.
- [ ] Centripetal (not uniform) Catmull-Rom used if waypoints are unevenly spaced,
      checked for no visible loops/cusps near close-together points.
- [ ] Tessellation density checked adaptively against actual on-screen curvature,
      not a single fixed segment count across all curve shapes.
