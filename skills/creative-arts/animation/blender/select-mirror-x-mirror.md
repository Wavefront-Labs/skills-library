---
id: creative-arts.animation.blender.select-mirror-x-mirror
name: select-mirror-x-mirror
category: creative-arts
field: animation
product: blender
tags: [blender, selection, select-mirror, x-mirror, mirror-editing, topology-mirror, symmetrize, symmetry]
level: practitioner
status: docs-checked
description: "Keep Blender meshes symmetric: Mesh Symmetry X/Y/Z and Topology Mirror, Select Mirror (Shift Ctrl M), Symmetrize direction and threshold, and Snap to Symmetry."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/tools/tool_settings.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/mirror.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/symmetrize.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/snap_symmetry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# select-mirror-x-mirror

Goal: keep full meshes symmetric while editing (for example after the Mirror modifier is applied, or for rigged characters).

## Mesh Symmetry (Sidebar > Tool tab > Options > Mirror)

- **X / Y / Z** toggles: when an element is transformed, its exact mirrored counterpart (in local space), if present, is transformed to match. Mirrored vertices must be precisely aligned with their counterparts or the mirror axis will not recognise them.
- **Topology Mirror**: finds mirrored vertices from their relationships with other vertices instead of positions, so slightly asymmetric meshes still mirror. It needs at least one mirror axis enabled, and works best with detailed geometry (simple cubes or UV spheres may give inconsistent results).
- The Mirror modifier symmetrizes non-destructively and avoids the strict alignment requirement.

## Select Mirror (`Shift Ctrl M`, Select > Select Mirror)

- Flips the selection to the opposite side of the mesh around a local axis, using the object origin as the centre. **Extend** adds to the selection instead of replacing it. Hold `Shift` to pick several axes: without Extend it mirrors once across the combination, with Extend across every combination.

## Repairing asymmetry

- **Symmetrize** (Mesh > Symmetrize): cuts at the object origin like Bisect, deletes one side, copies and mirrors the other side, then merges vertices on the plane. **Direction** (for example -X to +X deletes the positive-X geometry and replaces it with a mirrored copy of the negative side, in local space) and **Threshold** (vertices in range snap to the plane).
- **Snap to Symmetry** (Mesh > Snap to Symmetry): matches vertex pairs by position and repositions them without changing topology. **Direction**, **Threshold** (search radius), **Factor** (1: both take the "from" side's position; 0: the "to" side's; 0.5: the average), **Center** (moves vertices near the plane exactly onto it).
- Mesh > Mirror only flips the mesh without cutting or copying.

## Gotchas

- Mirror editing assumes symmetry about the object's local axes; keep the origin on the symmetry plane.
- Centre vertices slightly off the plane break pairing; run Snap to Symmetry with Center first.

## Verify

Move a vertex with X mirror on: its partner moves; Select Mirror selects one partner per vertex.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Tool Settings, Select Mirror, Symmetrize and Snap to Symmetry pages. Corrected the location of the mirror toggles (Sidebar Tool tab Options). Removed unconfirmed claims about sculpt, weight paint and shape key mirroring, the asymmetry-check recipe and UV behaviour after Symmetrize.
Method: documentation only; no commands were run.
