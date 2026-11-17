---
id: creative-arts.animation.blender.boolean-cleanup
name: boolean-cleanup
category: creative-arts
field: animation
product: blender
tags: [blender, boolean-cleanup, boolean-ngons, boolean-artifacts, hard-surface, weighted-normal, mesh-cleanup]
level: advanced
status: docs-checked
description: "Clean boolean results: ngon shading artefacts, limited dissolve, knife routing into quads, weighted and transferred normals, and prepping for subdivision or export."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/weighted_normal.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/smooth_by_angle.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/data_transfer.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# boolean-cleanup

Goal: boolean-cut surfaces that shade like the uncut shape and survive subdivision or export.

## Shading fixes (no topology change)

- **Weighted Normal** modifier (*Weighting Mode: Face Area*, *Keep Sharp* on) after Boolean and Bevel: larger faces get more weight in the combined normal, which flattens shading on big faces. *Face Influence* additionally uses the Weak/Medium/Strong strengths set with *Mesh > Normals > Set Face Strength*.
- **Data Transfer custom normals** from an uncut copy of a curved surface: the cut area inherits smooth normals (Face Corner Data → Custom Normals, Nearest Face Interpolated).
- The *Smooth by Angle* modifier (added by *Object > Shade Auto Smooth*) sets sharpness from the angle between neighbouring faces.

## Topology clean-up after applying

1. *Mesh → Clean up → Limited Dissolve* with a small angle to remove needless edges on flat areas.
2. Route ngons into quads with the Knife tool or *Vertex → Connect Vertex Path* (`J`) from the cut's corners to existing edges.
3. Remove doubled vertices (`M → By Distance`) and degenerate faces (`creative-arts.animation.blender.degenerate-dissolve`).
4. For subdivision: add support loops around the cut (`creative-arts.animation.blender.holding-edges`).

## Preventing artefacts

- Give curved bases enough segments before cutting so cut edges have vertices to land on.
- Keep cutter edges away from existing edges by small distances (slivers form otherwise).

## Gotchas

- Ngons on flat faces are fine for rendering without subdivision; do not over-clean.
- Ngons on curved faces always shade badly; fix normals or topology.
- Triangulate exports deterministically after cleanup (Triangulate modifier).

## Verify

Matcap view shows no gradients or dark smears around cuts; Subdivision preview (if used) stays clean; export triangle count is as expected.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST). Confirmed: Weighted Normal options (Weighting Mode with Face Area, Keep Sharp, Face Influence using Set Face Strength); Smooth by Angle is a modifier added by Shade Auto Smooth; Mesh > Clean up > Limited Dissolve; Vertex > Connect Vertex Path is J; Merge > By Distance on M; Data Transfer Face Corner Data > Custom Normals with Nearest Face Interpolated. Removed: the Auto Smooth reference, the Knife key and the numeric dissolve angle, which no manual page states. Corrected: Face Influence does not make big faces dominate (Face Area weighting does).

Method: documentation only; no commands were run.
