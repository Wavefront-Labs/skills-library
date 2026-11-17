---
id: creative-arts.animation.texturing.texture-atlases
name: texture-atlases
category: creative-arts
field: animation
product: texturing
tags: [texture-atlas, atlas, packing, draw-calls, trim-sheet, uv-layout, texturing]
level: practitioner
status: draft
description: "Combine textures into atlases: when it helps, layout and padding, mip-safe borders, atlas versus trim sheet versus texture array, and export naming."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Texture atlases

A **texture atlas** puts many separate textures (props, UI icons, sprite frames) into one larger image so they share a material.

## Why use one
- Fewer materials and draw calls in real-time engines, or fewer files to manage.
- Sprites and UI icons: one sheet with frame coordinates (`sprite-sheet-export.md`).
- Some offline pipelines use atlases to simplify asset handoff, but modern offline renderers rarely need them.

## Atlas versus alternatives
- **Trim sheet**: a texture of reusable strips (edges, panels, trim) that many assets map onto by UV placement; efficient for hard-surface sets.
- **Texture array** or **UDIM**: a set of same-size layers or tiles, with no neighbouring pixels to bleed (`udim-tiles-and-workflow.md`).
- Atlases cannot tile: UVs of a tiling texture break at the edge of its atlas cell.

## Layout
1. Choose the atlas size (power of two), and an even **texel density** for items (`texel-density-planning.md`).
2. Pack cells with **padding** and extend edge pixels into the padding (dilate) so filtering and mip-maps do not mix neighbours (`uv-packing-and-padding.md`).
3. Group by material type (all opaque PBR together, glass separate) and by update frequency.
4. Store the layout (name, x, y, w, h) in a JSON or the engine's atlas asset so scripts and tools can address cells.

## Gotchas
- Mip-map bleeding makes seams or colour fringing on small items; pad generously for distant objects.
- A single large atlas can waste memory when only some items are used on screen; consider multiple atlases.
- Changing one item may mean regenerating the atlas, and all assets using it.

## Verify
- [ ] Each cell has dilated padding; no neighbour bleed at the smallest mip used.
- [ ] Layout file generated with the atlas.
