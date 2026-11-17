---
id: creative-arts.animation.blender.poly-build-tool
name: poly-build-tool
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-editing, poly-build, polybuild, retopology, quad-draw, snapping, poly-build-retopo]
level: practitioner
status: docs-checked
description: "Model face by face with Blender's Poly Build tool: Ctrl LMB adds geometry, Shift LMB deletes, drag moves vertices or extrudes edges; Create Quads and retopology setup."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/tools/poly_build.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# poly-build-tool

Goal: place and connect faces one at a time; Poly Build combines several mesh editing tools into one and is especially useful for retopology.

## Controls (Edit Mode, Toolbar > Poly Build)

- **Ctrl LMB** adds geometry: creates a vertex at the cursor and a triangle with the nearest existing edge; if that edge already has two neighbouring faces, it makes an edge to the nearest existing vertex instead. Holding Ctrl previews in blue.
- **Shift LMB** dissolves the vertex or deletes the face under the cursor; holding Shift highlights the target in red.
- **LMB drag** a vertex to move it; **LMB drag** an edge to extrude it into a quad.

## Tool settings

- **Create Quads**: when a new triangle shares an edge with an existing one, that edge is dissolved so a quad remains.
- The manual suggests enabling Snapping and Auto Merge (Sidebar > Tool > Options) while tweaking vertices so they combine.

## Retopology workflow

1. Create a new mesh overlapping the original and adjust it until it covers the original's shape.
2. Use the Retopology overlay in the 3D Viewport to see the original through the new mesh without X-Ray clutter from the far side.
3. Use Snapping to align new vertices to the original mesh.
4. Lay the main loops first (eyes, mouth, joints), then fill.

## Gotchas

- Without snapping, new vertices land on the view plane and can drift off the surface.
- Merge distant vertices with `M` or Auto Merge.

## Verify

Face count and topology as planned; Non Manifold selection only on intended borders.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Poly Build and Remeshing (Retopology) pages: Ctrl/Shift/LMB behaviours, Create Quads, Retopology overlay and snapping advice. Removed unconfirmed snap target names, Shrinkwrap/Mirror workflow steps and the overlay version note.
Method: documentation only; no commands were run.
