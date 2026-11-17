---
id: creative-arts.animation.blender.auto-masking-options
name: auto-masking-options
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, auto-masking-options, auto-masking-topology, auto-masking-cavity, view-normal-masking, auto-masking, front-faces-only]
level: practitioner
status: docs-checked
description: "Use Blender sculpt Auto-Masking to protect geometry without painting masks: topology, face sets, boundaries, cavity with curve, view and area normal, global versus per-brush."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/controls.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/brush_settings.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/mask.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# auto-masking-options

Goal: brushes automatically limited to the right region, with no stroke leakage onto lips, fingers or the back side.

## Where it lives

Sculpt Mode header > Auto-Masking popover, or the Auto-Masking pie menu on Alt-A. The same toggles also exist per brush in Sidebar > Tool > Brush Settings > Advanced > Auto-Masking, so a brush can have its own behaviour. Auto-masks are generated at the start of every stroke or tool use and are never shown as an overlay. All modes can be combined.

## Options

- **Topology**: only vertices connected to where the stroke started are affected, so loose islands are masked out. For Grab and Thumb, anything not connected within the brush radius is also masked.
- **Face Sets**: only the face set under the cursor at stroke start.
- **Mesh Boundary** and **Face Sets Boundary**: vertices on open boundary edges (or between face sets) are not affected; this includes boundaries to hidden faces. **Propagation Steps** widens the soft gradient toward those boundaries and is shared by both. **Create Mask** runs the matching Mask from Boundary operator with the current settings, which is a quick way to see the auto-mask.
- **Cavity** and **Cavity (Inverted)**: Cavity leaves the peaks of the surface curvature unaffected; the inverted version leaves the crevices unaffected. They cannot be on together and share settings: **Factor** (contrast, default 0.5), **Blur** (blur passes; 0 gives the pure cavity mask), **Custom Curve**. **Create Mask** runs Mask from Cavity. Cavity is aimed mainly at painting but also works for sculpting.
- **View Normal**: only vertices whose normal faces the viewer. **Limit** sets the angle range (90 degrees covers everything visible) and **Falloff** extends it softly. **Occlusion** restricts to vertices not hidden by other faces; it is incompatible with Limit and Falloff and is much slower.
- **Area Normal**: like View Normal but uses the surface normal at the stroke start, with the same Limit and Falloff.

If nothing is under the cursor at stroke start for Topology or Face Sets, the previously auto-masked area is targeted again, which helps with the Projected falloff shape.

## Recipes

- Sculpt one lip without touching the other: lips that touch share topology, so use Face Sets (Initialize Face Sets, or paint sets) plus Face Sets auto-masking, and add Face Sets Boundary to keep the set borders fixed.
- Grime in crevices: use a painting brush with Cavity or Cavity (Inverted) and shape the response with Custom Curve.

## Gotchas

- Topology and Face Sets sample at stroke start; starting on the wrong part masks the wrong region.
- Occlusion costs performance; prefer View Normal with a Limit when it is enough.

## Verify

Stroke across a boundary: the protected region stays unchanged. Toggle the option off and on to compare. Use Create Mask on Cavity or the boundary options to see what the auto-mask would cover.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch of the manual repository). Confirmed against sculpt_paint/sculpting/controls and sculpt_paint/brush/brush_settings: Alt-A pie and header popover, per-brush Advanced panel, each option name, Propagation Steps shared by both boundary modes, Cavity Factor default 0.5 and Blur, Cavity and Cavity (Inverted) exclusivity, View Normal Limit/Falloff/Occlusion behaviour, Area Normal, Create Mask buttons. Removed unconfirmed wording about how global and brush settings combine.
Method: documentation only; no commands were run.
