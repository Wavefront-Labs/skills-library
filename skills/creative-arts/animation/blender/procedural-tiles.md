---
id: creative-arts.animation.blender.procedural-tiles
name: procedural-tiles
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, procedural-tiles, tiles-shader, grout]
level: practitioner
status: docs-checked
description: "Create procedural tiles and grout in Blender: Brick Texture vs fraction/floor maths, per-tile random colour, grout mask and bevelled bump."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/brick.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# procedural-tiles

## Square tiles with vector maths

1. Take UV or Object coordinates and multiply by the tile count.
2. The **fractional part** gives per-tile local coordinates (0 to 1); the **floor** gives an integer tile ID.
3. Grout mask: subtract 0.5 from the local coordinates, take the absolute value, then the larger of X and Y, and remap a narrow band near the tile edge to 0..1 so the grout has a soft edge.
4. Per-tile random: feed the tile ID (never the raw coordinates) into a white-noise style random node, then drive a colour ramp or hue offset.
5. Bump: pass the grout mask through a smooth ramp into a Bump node for bevelled tile edges.

## Brick Texture node

The *Brick Texture* node produces bricks procedurally. Inputs: *Color 1/2* (brick colours), *Mortar* (colour between bricks), *Scale*, *Mortar Size* (0 means no mortar), *Mortar Smooth* (softens the mortar/brick edge, useful with displacement), *Bias* (colour variation between Color 1 and 2: -1 and 1 use only one colour, values between mix them), *Brick Width* and *Row Height* (ratios relative to the texture scale). Properties: *Offset* (row offset) with its *Frequency*, and *Squash* with its *Frequency* (narrower or wider bricks on some rows). Outputs: *Color* and *Factor*, where Factor is the mortar mask (1 = mortar).

For square tiles set the row offset to zero and make Row Height match Brick Width; use Factor as the grout mask and Bias to vary the tint per tile. The node is limited to rectangular grids.

## Other layouts

- Hexagons: a Voronoi-based or hex-grid maths setup.
- Herringbone / basketweave: maths on the tile IDs (swap axes on alternate cells), or image textures.

## Grout material

Mix by the grout mask: a darker, rougher grout material, slightly recessed via bump, with dirt from an ambient occlusion node if wanted.

## Gotchas

- Tiles misaligned with geometry: apply scale and align UVs to edges.
- Per-tile random values must come from tile IDs, not raw coordinates.

## Verify

Tiles are exactly N per metre, grout is constant width, and each tile is slightly different in colour.

## Checked

2026-11-09. Confirmed against the Blender manual Brick Texture node page (raw RST, read in full): all inputs, properties and outputs named above, including Factor as the mortar mask and the Bias behaviour. Removed: the specific values 0.02, 0.47 to 0.5 and roughness 0.9, exact node names in the vector-maths chain (maths described generically, not claimed as node names), and the Voronoi Randomness 0 hexagon recipe (not on the page).
Method: documentation only; no commands were run.
