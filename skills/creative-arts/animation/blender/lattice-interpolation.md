---
id: creative-arts.animation.blender.lattice-interpolation
name: lattice-interpolation
category: creative-arts
field: animation
product: blender
tags: [blender, lattice, lattice-interpolation, lattice-bspline, cardinal, linear, deformation]
level: practitioner
status: docs-checked
description: "Choose Blender lattice interpolation per axis: Linear, Cardinal, Catmull-Rom, BSpline — how each shapes the deformation, overshoot, and matching it to resolution."
sources:
  - https://docs.blender.org/manual/en/latest/animation/lattice.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# lattice-interpolation

Goal: deformations that are as smooth (or as hard) as intended between lattice points.

## Interpolation type (Lattice Data > Lattice panel, per axis U/V/W)

The manual lists four types per axis: Linear, Cardinal, Catmull-Rom and B-Spline (see its interpolation figure). The comparisons below are practice observations, not manual text; test them on your own lattice.

| Type | Typical behaviour | Use |
|---|---|---|
| Linear | straight blends between points | mechanical/hard taper, exact control |
| Cardinal | smooth curve | moderate smooth bends |
| Catmull-Rom | smooth curve | smooth with predictable passes |
| B-Spline | approximating spline, usually the smoothest | squash/stretch, organic bulges |

- The interpolation type is set separately for each axis (U, V, W), so a smooth type can be used along one axis and Linear across the others.

## Pairing with resolution

- Resolution (Points U, V, W) is 1 to 64 per axis in the Python API; with only two points along an axis there is little for the interpolation type to do (practice).
- Higher resolution gives more local control but more points to manage (practice).

## Gotchas

- Changing interpolation changes the shape of an existing deformation; compare before committing on animated lattices (practice).
- Lattice modifier *Strength* (and vertex group) blends the whole deformation; interpolation only changes shape.

## Verify

Move the middle point of a 3-point axis and switch between the interpolation types to compare how the mesh follows it.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against animation/lattice.rst (Interpolation Type selector per axis with Linear, Cardinal, Catmull-Rom, B-Spline; Points U, V, W) and rna_lattice.cc (points range 1 to 64, per-axis interpolation properties; source main on this date). Removed unconfirmed default type and behaviour claims, reframed the comparison as practice.

Method: documentation only; no commands were run.
