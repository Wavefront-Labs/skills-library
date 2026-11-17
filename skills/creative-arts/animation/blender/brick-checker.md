---
id: creative-arts.animation.blender.brick-checker
name: brick-checker
category: creative-arts
field: animation
product: blender
tags: [blender, procedural-texturing, brick-checker, brick-texture, checker-texture]
level: practitioner
status: docs-checked
description: "Use Blender Brick and Checker textures: brick offset, frequency, squash, mortar size and smooth, bias, row height, and checker scale for test patterns."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/brick.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/textures/checker.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# brick-checker

## Brick Texture

- Properties: **Offset** (row offset), **Frequency** (how often rows are offset; 2 gives an even/uneven pattern), **Squash** (adjusts brick width for particular rows) and a second **Frequency** (labelled Squash Frequency in the node; how often rows consist of squished bricks).
- Inputs: **Color 1/2**, **Mortar**, **Scale**, **Mortar Size** (0 = no mortar), **Mortar Smooth** (softens the mortar edge; useful for bump and displacement), **Bias** (colour variation; -1 and 1 use only one of the two colours), **Brick Width** and **Row Height** (ratios relative to the texture Scale).
- Outputs: **Color** and **Factor** (mortar mask, 1 = mortar). Use Factor for bump and mortar roughness.

## Checker Texture

- Inputs: **Vector** (defaults to Generated coordinates when unconnected), **Color1**, **Color 2**, **Scale** (for example 15 gives 15 alternate patterns over the UV bounding box). No properties.
- Outputs: **Color** and **Factor** (Checker 1 mask, 1 = Checker 1).
- Use as a UV check (stretching, texel density), a camera-tracking test floor, chessboards or retro floors.

## Recipes

- Brick wall: Factor (mortar mask) into a Bump node for recessed mortar; Color output through Hue/Saturation for per-brick variation.

## Gotchas

- Brick Width and Row Height are relative to Scale, not absolute sizes.
- The Checker node can show precision issues with some vector inputs (see the White Noise Texture notes in the manual).

## Verify

Measure a brick against a known-size reference object in the viewport; mortar is visible in the bump result.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against textures/brick and textures/checker: input, property and output names (Factor output), Bias behaviour, Mortar Size 0, Brick Width/Row Height ratios, Checker Vector default, Factor meaning and precision warning. Removed the 0.5 running-bond default, the numeric recipe values, the herringbone remark, the 2D-coordinates claim and the real-size example.

Method: documentation only; no commands were run.
