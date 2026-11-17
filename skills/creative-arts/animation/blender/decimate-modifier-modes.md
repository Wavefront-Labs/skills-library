---
id: creative-arts.animation.blender.decimate-modifier-modes
name: decimate-modifier-modes
category: creative-arts
field: animation
product: blender
tags: [blender, decimate, modifiers, collapse, un-subdivide, planar, polycount]
level: practitioner
status: verified
description: "Reduce polycount with Blender's Decimate modifier: Collapse (ratio, symmetry, triangulate), Un-Subdivide (iterations) and Planar (angle limit, delimit)."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/decimate.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# decimate-modifier-modes

Goal: fewer polygons with the least visible damage. Intended for meshes from sculpting, complex modeling or applied Subdivision Surface/Multiresolution modifiers, not for carefully economical models. Unlike most modifiers, its result is not shown in Edit Mode; the modifier panel shows the number of remaining faces.

## Collapse

Merges vertices progressively, taking the shape into account.
- **Ratio**: fraction of faces kept (1.0 unchanged, 0.5 half, 0.0 none). Triangles are used when calculating the ratio, so with Triangulate off, quads and other polygons that are not collapsed leave more faces than expected.
- **Symmetry**: maintains symmetry on one axis.
- **Triangulate**: keeps resulting triangulated geometry.
- **Vertex Group** + **Factor**: a vertex group controls which parts are decimated, and Factor sets its influence.

## Un-Subdivide

The reverse of subdivide: removes edges that came from a subdivide operation. For mainly grid-based topology; results may be unexpected if the mesh was edited after subdividing.
- **Iterations**: two iterations equal one subdivide, so use even numbers.

## Planar

Reduces detail on mostly flat forms.
- **Angle Limit**: dissolves geometry forming angles higher than the setting.
- **Delimit**: Normal, Material, Seam, Sharp, UVs; no dissolving at those borders.
- **All Boundaries**: dissolves all vertices along face boundaries; the manual says this can help with a high Angle Limit.

## Verify

Check the face count shown under the modifier, and compare silhouettes at the target viewing distance.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Decimate page). Confirmed: three modes and their option names, ratio and triangle note, even-iterations advice, delimit options. Removed unconfirmed default angle, UV/scale gotchas and the Limited Dissolve equivalence.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Decimate with Python: modes Collapse (default), Un-Subdivide and Planar; Delimit has Normal, Material, Seam, Sharp, UVs; defaults Ratio 1.0, Iterations 0, Angle Limit 5 degrees, Symmetry axes X/Y/Z; on a 400-quad grid Ratio 0.5 gave 203 faces (the panel Face Count property reports it), Ratio 1.0 kept 400 and Ratio 0 gave 0; Triangulate on gave 400 triangles at Ratio 0.5 with quads removed; Un-Subdivide on a twice-subdivided cube (96 faces) gave 48, 24 and 12 faces for 1, 2 and 3 iterations, so two iterations undo one subdivision; Vertex Group with Factor 0 and 1 gave different results (148 and 220 faces); Planar on a flat grid collapsed it to 1 face and All Boundaries removed more. Not run: the Edit Mode hidden-result claim and Symmetry shape effects.

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
