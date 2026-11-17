---
id: creative-arts.animation.blender.cast-modifier
name: cast-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, cast-modifier, modifiers, deform, to-sphere, spherify]
level: practitioner
status: verified
description: "Push geometry toward a sphere, cylinder or cuboid with Blender's Cast modifier: factor, radius, size, axis toggles, control object and vertex group."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/cast.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# cast-modifier

Goal: morph a mesh (or curve, surface, lattice) toward a primitive shape with an animatable amount: inflating a cube into a ball, rounding a chunky model, pulsing bubbles. It is the non-destructive equivalent of the Edit Mode *To Sphere* tool.

## Fields

- **Shape**: *Sphere*, *Cylinder* or *Cuboid*.
- **Axis** (X, Y, Z toggles): which axes are affected. For *Cylinder* only X and Y are offered; Z stays unaffected.
- **Factor** (default 0.5): linear blend between original (0.0, no effect) and cast (1.0) positions. Values below 0 or above 1 exaggerate the deformation.
- **Radius**: if nonzero, defines a sphere of influence; vertices outside it are not affected.
- **Size**: alternative size of the projected shape; if zero it comes from the initial shape and the control object.
- **Size from Radius**: calculates Size from Radius for smoother results.
- **Vertex Group** (+ Invert): restrict the effect by painted weights.
- **Object**: control object. Its origin location defines the centre of the projection; its size and rotation transform the projected vertices. Keyframing it animates the deformation.

## Recipes

- **Cube to ball**: subdivide the cube, Cast Sphere, keyframe Factor 0 to 1.
- **Rounded dice**: Cast Cuboid on a dense sphere.
- **Smoothing**: the manual suggests the Smooth modifier as a companion, since the cast shape sometimes needs smoothing to fix shading artefacts.

## Gotchas

- The modifier works only with local coordinates for performance; apply object transformations if the result looks wrong, especially for Cylinder.
- Without a control object the centre is the object origin, so a mesh with its origin at the base casts lopsided.
- Few vertices give a faceted result; add subdivision first.

## Verify

Factor 0 matches the base mesh; Factor 1 with the Sphere shape puts every affected vertex at the same distance from the centre.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Cast modifier page). Confirmed: option names (Shape, Axis, Factor, Radius, Size, Size from Radius, Vertex Group, Object), factor semantics, cylinder X/Y only, local-coordinates note. Removed unconfirmed default values, the "Use Transform" option and unconfirmed recipes.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: Shape enum Sphere, Cylinder, Cuboid; Factor 1 on a subdivided cube put every vertex at one distance from the centre (1.3041 min and max); Factor 0 left it unchanged; Factor 1.5 overshot (distances spread 1.09 to 1.44); Cylinder left Z untouched; with Radius 1.2 no vertex farther than 1.2 moved; a control object at another location re-centred the projection; X/Y/Z axis toggles exist.

Method: manual text confirmed from documentation; Cast behaviour run headless in Blender 4.5.14.
