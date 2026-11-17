---
id: creative-arts.animation.blender.uv-sync-selection
name: uv-sync-selection
category: creative-arts
field: animation
product: blender
tags: [blender, uv, uv-editor, uv-sync-selection, sticky-selection, island-select, uv-selection]
level: practitioner
status: docs-checked
description: "Control UV selection in Blender 5.2: Sync Selection (on by default), select modes 1-4 including Island, and Sticky Selection (Shared Location, Shared Vertex, Disabled)."
sources:
  - https://docs.blender.org/manual/en/latest/editors/uv/selecting.html
  - https://docs.blender.org/manual/en/latest/editors/uv/introduction.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# uv-sync-selection

Goal: select the UVs you mean, not their hidden neighbours or the whole island by accident.

## Sync Selection (UV Editor header)

- **On (the default in 5.2)**: the UV Editor and 3D Viewport share a selection. All faces are visible in the UV Editor. Selecting in the 3D Viewport selects all corresponding UV elements; selecting a UV selects the mesh element. In vertex and edge modes only some of the UVs attached to a vertex may be selected.
- **Off**: only UVs of faces selected in the 3D Viewport are shown. UV selection is independent, so single UV vertices or edges can be selected even if they belong to the same mesh vertex or edge; selecting in one editor no longer affects the other.
- Only some 3D Viewport selection operations keep per-UV selection (basic picking, box, circle and lasso); others such as Select Random or Select Similar reset it so all UVs of the selected mesh elements become selected.
- With Sync on, `Shift` clicking a selection-mode button enables several modes at once.

## Selection modes

- Vertex `1`, Edge `2`, Face `3`, and **UV Island Selection** `4` (selects contiguous groups of faces connected in the UV map).

## Sticky Selection Mode (UV Editor header)

- **Shared Location** (default): selects UV vertices of the same mesh vertex that have the same UV coordinates, which makes overlapping vertices behave as shared.
- **Shared Vertex**: selects all UV vertices of the same mesh vertex, even at different UV coordinates; moving a seam vertex drags its copies on other islands.
- **Disabled**: each UV vertex is selected independently; needed to split UVs by hand.

## Other selection tools

- Select > All `A`, None `Alt A`, Invert `Ctrl I`, Box `Alt B`, Box Select Pinned `Ctrl B`, More/Less `Ctrl NumpadPlus` / `Ctrl NumpadMinus`, All by Trait (Tile, Pinned `Shift P`, Overlap, Winding), Select Similar `Shift G`.

## Gotchas

- "I moved a vertex and it tore": Sticky Selection is Disabled. "Moving one island drags another": Shared Vertex.
- Rip Move UV needs Sync Selection off.

## Verify

Select one UV vertex on a seam under each sticky mode and watch which corners highlight.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Selecting UVs, UV Editor introduction and UV Operators pages. Corrected: Sync Selection defaults to on in 5.2 (the old text said off); sticky mode names and semantics; island selection is a select mode (4). Removed unconfirmed linked-select and hidden-face remarks.
Method: documentation only; no commands were run.
