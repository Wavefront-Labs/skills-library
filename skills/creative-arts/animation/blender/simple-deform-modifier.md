---
id: creative-arts.animation.blender.simple-deform-modifier
name: simple-deform-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, simple-deform-modifier, twist, taper, bend, stretch-deform, simple-deform, modifiers, origin-empty]
level: practitioner
status: verified
description: "Use Blender's Simple Deform modifier for twist, bend, taper and stretch: set axis, limits, origin empty and vertex group, with enough edge loops so the deformation is smooth."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/simple_deform.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# simple-deform-modifier

Goal: bend a pipe into an elbow, twist a cable, taper a horn or stretch a spring non-destructively, and animate it.

## Modes

| Mode | Parameter | Behaviour |
|---|---|---|
| **Twist** | Angle | Rotates the mesh around the axis; the rotation at each vertex is weighted by its distance from the origin along the axis (vertices in the origin's plane do not rotate). |
| **Bend** | Angle | Bends the mesh over the axis; the bending axis is paired with the deform axis (see below). |
| **Taper** | Factor | Scales linearly along the axis, weighted by distance from the origin; no scaling in the origin's plane. |
| **Stretch** | Factor | Stretches along the axis; with a positive factor the mesh gets longer, wider at the borders and thinner at the origin; negative squashes it. |

Angle (Twist, Bend) or Factor (Taper, Stretch) is the total amount and can be negative to reverse the deformation.

**Axis** (X, Y or Z, in the object's local space): the deform axis. For Bend the manual pairs the deform axis with a bending axis: X with Z, Y with Z, Z with X. A flat plane with deform axis X or Y therefore shows no bend, because all its vertices share the bending-axis coordinate.

**Origin**: an object (usually an Empty) that defines the origin and axis of deformation. Rotating it controls the axis (its local axis is used), moving it controls the origin, and scaling it changes the deformation factor. Without it, the modified object's own origin is used.

**Restrictions**: *Limits* (lower and upper limit mapped onto the deform axis, measured from the object origin; the upper limit cannot be lower than the lower), *Lock* (Twist, Taper and Stretch only; controls whether the coordinates along the two other axes may change), *Vertex Group* for per-vertex influence.

## Geometry requirements

The modifier moves existing vertices, so a mesh with only a couple of loops across the bent span cannot bend smoothly (practice). Add loops with Loop Cut or put a *Subdivision Surface (Simple)* before Simple Deform.

## Recipes

These recipes are practice, not from the manual; tune the values by eye.

- **Elbow pipe**: a densely looped cylinder, Simple Deform Bend with the matching axis, Origin empty at the base. Keyframe Angle for a growing bend.
- **Twisted rope**: array of a short segment, Simple Deform Twist over the whole length, then a Curve modifier to lay it on a path (Twist before Curve).
- **Horn**: a tube with stacked Simple Deforms (Taper, Twist, Bend).
- **Spring compression**: animate Stretch Factor on a helix.

## Gotchas

- The deformation is calculated in local space and the axes of an object can differ from the global ones; check the object's rotation if the axis looks wrong.
- The vertices furthest from the origin along the deform axis represent the upper and lower limits, so a stray far-away vertex changes the effective span.
- Applying object scale first (Object, Apply, Scale) avoids uneven results (practice).

## Verify

- Wireframe: deformed loops stay evenly spaced.
- Set Angle or Factor to zero and confirm the mesh looks undeformed.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/modifiers/deform/simple_deform.rst: four modes and their behaviour, deform/bending axis pairs (X-Z, Y-Z, Z-X), Origin object (rotate, move, scale), Limits, Lock (Twist, Taper and Stretch only), Vertex Group, local-space note. Removed unconfirmed taper factor values, loop-count rules of thumb, dependency-cycle and Subdivision-order claims; recipe values are practice.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: the mode enum is Twist, Bend, Taper, Stretch (default Twist, axis X, angle and factor 45 degrees / 0.785); on a flat XY plane Bend with deform axis X or Y moved nothing (largest displacement 0) and with Z moved vertices by up to 0.9, matching the axis pairing; Angle 0 and Taper Factor 0 leave the mesh unchanged; Stretch +0.5 on X lengthened the plane from +-1 to +-1.25 with the width 0.75 at the origin against 1.0 at the border, and -0.5 shortened it to +-0.75; Limits is a two-value range.

Method: manual text confirmed from documentation; Simple Deform behaviour run headless in Blender 4.5.14.
