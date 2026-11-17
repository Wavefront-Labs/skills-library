---
id: creative-arts.animation.blender.screw-profile
name: screw-profile
category: creative-arts
field: animation
product: blender
tags: [blender, screw-profile, screw-steps, screw-axis, screw-modifier, modifiers, lathe, revolve, threads, springs]
level: practitioner
status: docs-checked
description: "Build lathes, springs and threads with Blender's Screw modifier: Angle, Screw, Iterations, Axis Object, Steps, Merge, Stretch UVs, Calculate Order, and the Edit Mode operator."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/screw.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/screw.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# screw-profile

Goal: a non-destructive lathe or helix (vases, bottles, wheels, bolts, springs, spiral stairs) from a profile object, using the Screw modifier. The profile can be a mesh or a curve; faces are not required.

## Profile and axis

- The modifier builds a helix-like shape from the object's own geometry. Align the profile to the cardinal direction of the object, not to the screw axis; proper alignment of the profile is important.
- **Axis** sets the axis along which the helix is built. **Axis Object** names an object that defines the axis direction; with **Object Screw** on, the distance from the Axis Object defines the height of one helix iteration.

## Fields

- **Angle**: degrees of a single helix revolution (360 for a full revolve; smaller for a partial one).
- **Screw**: height of one helix iteration.
- **Iterations**: number of revolutions.
- **Steps Viewport / Render**: steps per revolution in the viewport and at render time; increase Render for quality.
- **Merge** (+ **Merge Distance**): merges vertices that lie on the axis of rotation, closing end points with a triangle fan; vertices closer than the distance to the axis are merged.
- **Stretch UVs**: stretches UVs from 0 to 1 when UVs are present.
- **Normals**: **Smooth Shading** (output faces smooth shaded; shading of the input is not preserved), **Calculate Order** (orders edges to avoid normal and shading problems; only needed for meshes, not curves), **Flip** (flip normals).

## Edit Mode Screw operator (Edge > Screw)

The operator extrudes selected geometry along a helix. Differences from the modifier: it works in world space, extrudes only the selection, takes a manual centre point, always uses 360 degree turns, and derives height and radial offset per turn from the open profile in the selection. See `spin-screw-tools`.

## Recipes (set values to taste)

- **Vase or bottle**: a single-line profile beside the axis, Angle 360, Screw 0 for a lathe, Merge on so axis vertices close; add a Solidify modifier afterwards if the profile is an open line and you want thickness.
- **Thread or spring**: give Screw a height per turn and Iterations the number of turns; use the Edit Mode operator when the height should follow the profile geometry.

## Gotchas

- A mis-aligned profile gives the wrong axis result; fix alignment before changing Axis.
- Inverted or black shading: try Calculate Order (meshes) or Flip.
- Check the render-step count in Rendered view as well as the viewport.

## Verify

Face Orientation overlay shows only the front colour; the wireframe shows no doubled seam where Merge applies.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Screw Modifier and Screw (Edit Mode) pages: every field name and meaning, Normals options, operator comparison table. Corrected: Merge joins vertices on the rotation axis (it does not weld first and last step); the setting is Stretch UVs (single toggle); Axis Object and Object Screw meaning. Removed unconfirmed step counts, pitch figures, face-count formula and rotation gotchas.
Method: documentation only; no commands were run.
