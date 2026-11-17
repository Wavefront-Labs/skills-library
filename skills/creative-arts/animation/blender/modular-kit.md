---
id: creative-arts.animation.blender.modular-kit
name: modular-kit
category: creative-arts
field: animation
product: blender
tags: [blender, modular-kit, modular-assets, modular-building, environment-modeling, snapping, grid]
level: practitioner
status: docs-checked
description: "Build a modular environment kit in Blender: grid size and pivot rules, absolute grid snapping, matching seams, collection instances for assembly."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/controls/snapping.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/properties/instancing/collection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# modular-kit

Goal: walls, floors, doorways and trims that snap together with no gaps, reusable across scenes and engines.

## Grid and dimensions

- Pick one base unit and stick to it (for example a 0.5 m grid with wall pieces in multiples of it). The exact numbers are your pipeline's choice.
- Every piece's dimensions are exact multiples of the grid unit, and the viewport grid is set to match, because Increment snapping uses the viewport grid resolution.

## Pivots

Put the origin at a consistent corner (for example bottom-left-back) or bottom-centre on every piece, so rotating by 90 degrees keeps pieces on the grid. Mixed pivot conventions are the most common kit-breaking error.

## Snapping for assembly

Snapping is toggled with the magnet icon in the 3D Viewport header, or temporarily by holding `Ctrl`.

- Snap Target *Increment* snaps to an imaginary grid that starts at the selection's original location; tick *Absolute Increment Snap* to snap to the viewport grid itself instead, so moves land exactly on grid points. Do not confuse it with the *Grid* target, which moves to the grid point closest to the mouse cursor.
- Or Snap Target *Vertex* with Snap Base *Closest* (the bounding-box corner in Object Mode, the vertex in Edit Mode) to join pieces corner to corner. Several targets can be combined with `Shift-LMB`.
- Snapping affects Move by default; it can also be enabled for Rotate and Scale (the *Affect* setting), and the rotation increment is configurable.

## Seams

- Edge vertices at piece borders sit exactly on the grid lines, with an identical profile at both ends of a wall so neighbours match.
- Avoid geometry crossing piece borders; trims and caps cover joins.
- Keep normals and UVs consistent at borders (see `creative-arts.animation.blender.environment-modeling`).

## Kit organisation

- One collection per piece (for example `KIT_wall_2m`).
- Assemble scenes with *Add > Collection Instance*. This creates an empty that instances the collection; duplicating the empty keeps its instance setting, and edits to the collection propagate to every instance. A collection linked from another blend-file does not appear in the scene until such an empty places it.
- To edit an instance as normal objects, select it and run the `bpy.ops.object.duplicates_make_real` operator; parent-child relationships do not carry over, and linked data stays linked.
- Export to engines with the same pivots (`creative-arts.animation.blender.batch-export-script`).

## Gotchas

- Bevel modifiers on border edges create visible gaps between neighbours; leave border edges unbevelled or bevel only exposed edges.
- Unapplied scale ruins snapping and exports; apply scale on every piece.

## Verify

Assemble a 3x3 room from pieces: no visible seams or light leaks in a render, and every piece's location values are exact grid multiples.

## Checked

2026-11-09. Confirmed against the Blender manual Snapping page and Instancing > Collection page (raw RST, both read in full): snap toggle and `Ctrl`, Snap Base Closest, Increment vs Grid targets, Absolute Increment Snap, `Shift-LMB` multiple targets, Affect, Add > Collection Instance, empties, linked collections, the duplicates_make_real operator. Removed: unit-scale and overlay-grid settings, Set Origin menu path, `R Z 90`, Instance Offset, asset marking and `Alt D` (not on the cited pages).
Method: documentation only; no commands were run.
