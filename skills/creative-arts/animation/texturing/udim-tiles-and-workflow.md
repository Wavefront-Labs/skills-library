---
id: creative-arts.animation.texturing.udim-tiles-and-workflow
name: udim-tiles-and-workflow
category: creative-arts
field: animation
product: texturing
tags: [udim, uv-tiles, uv-layout, texture-sets, tile-numbering, painter, blender, texturing]
level: practitioner
status: draft
description: "Work with UDIM tiles: numbering from 1001, layout in UV space, Painter's UV-tile workflow, file naming, Blender usage and common mismatches."
sources:
  - https://helpx.adobe.com/substance-3d-painter
  - https://www.blender.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# UDIM tiles

UDIM lays UVs across **multiple 0-1 tiles** along the U axis (and up the V axis), each tile with its own texture file. It lets a hero asset have more total resolution than one map allows, without a huge single image.

## Numbering
- Tile number = `1001 + U + 10 x V` where U and V are the integer tile coordinates.
- Tile 1001 is the standard 0-1 square, 1002 is the next one to the right (U 1-2), and 1011 is the first tile of the second row up (V 1-2).
- The format allows ten tiles along U (1001 to 1010), then wraps to the next row.

## Layout
- Move islands for each region (head, hands, torso) into their own tile; keep an island inside one tile and away from tile borders.
- Keep texel density consistent across tiles (`texel-density-planning.md`).

## Substance 3D Painter
- Create the project with the **UV tile workflow** enabled (in the new-project dialog, the UV Tiles option); each UDIM tile appears as a separate texture-set UV tile. Painter exports one file per tile.
- Export preset names include a UDIM token so the files come out as `name.1001.png`, `name.1002.png`; confirm the naming in the export preset (`painter-export-presets.md`).
- See `painter-texture-sets.md` for combining several tiles into a texture set.

## Blender
- Image Texture node: set the image source to **UDIM Tiles** (or use a filename with a UDIM tag when loading); tiles are listed in the image editor, and the UV Editor shows and edits several tiles.
- Rendering with UDIM is supported in Cycles; Eevee support depends on version.

## Gotchas
- A renderer or engine that does not support UDIM needs the tiles split into materials.
- Missing tile files render black or magenta; check that all tiles exist.
- Sets of maps must have matching tile sets across channels.

## Verify
- [ ] All tiles exist for every channel with the right number.
- [ ] Islands do not cross tile borders.
- [ ] A renderer test shows no seams at tile edges.
