---
id: creative-arts.animation.blender.magic-white-noise
name: magic-white-noise
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, magic-white-noise, magic-texture, white-noise, per-cell-random]
level: practitioner
status: docs-checked
description: "Use Blender Magic Texture for psychedelic interference patterns and White Noise Texture for per-cell or per-pixel random values in shaders, with the Snap cell-noise recipe."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/magic.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/white_noise.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# magic-white-noise

## Magic Texture

- Inputs **Vector** (defaults to Generated coordinates if unconnected), **Scale**, **Distortion**; property **Depth** (number of iterations). Outputs **Color** and **Factor**. The RGB components are generated independently with a sine formula.
- The manual notes it can imitate thin-film interference: assign a **Reflection** Texture Coordinate to Vector and use a relatively high Distortion (the manual text says "Turbulence", but the node's input is Distortion).
- Uses: iridescent colour fields, stylised energy, quick colourful variation (practice).

## White Noise Texture

- **Dimensions** 1D, 2D, 3D or 4D choose how the seed is built: 1D uses W, 2D uses the X and Y of Vector, 3D uses Vector, 4D uses Vector and W. Outputs **Value** and **Color**, each in 0 to 1.
- The slightest difference in seed gives a completely different output, so every distinct input gets a different random value.
- **Per-cell random**: the manual's example generates cell noise using the **Snap** vector operation (Vector Math) feeding a White Noise node, so the seed is constant within each cell.
- Precision: if results flicker at unit boundaries or at zero, the manual suggests lowering the dimension so a constant seed component is dropped (or multiplying it by zero), adding an arbitrary value to the seed, or taking the absolute value of the seed (signed zero).

## Recipes (practice)

- Random tile colours: Snap of (UV x tile count) into White Noise Color, then a Color Ramp palette.
- Random plank offset: row index through White Noise into Mapping location.

## Gotchas

- White noise on continuous coordinates is grainy; quantise the input first.
- Magic is hard to art-direct; restrict it with masks.

## Verify

Tile test: each tile is a uniform colour, neighbours differ, no pixel noise inside tiles.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release) render/shader_nodes/textures/magic.rst (inputs, Depth, outputs, thin-film tip, sine formula) and white_noise.rst (Dimensions behaviour, outputs, precision notes, Snap cell-noise example). Removed: Depth range "2-10", the Voronoi/Brick per-cell claims, and the Object Info Random alternative. Method: documentation only; no commands were run.
