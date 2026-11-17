---
id: creative-arts.animation.blender.gp-noise-modifier
name: gp-noise-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-noise-modifier, gp-noise, line-boil, gp-modifiers]
level: practitioner
status: docs-checked
description: "Add hand-drawn wobble and line boil to Grease Pencil with the Noise modifier: position/strength/thickness/UV factors, noise scale, seed and stepped randomness."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/deform/noise.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gp-noise-modifier

Goal: organic jitter on clean or Line Art strokes, static or boiling over time.

## Settings (Grease Pencil Noise modifier)

- **Position**, **Strength** (opacity), **Thickness**, **UV** (UV rotation): strength of the noise over each point property.
- **Noise Scale**: noise frequency scale. **Noise Offset**: moves the noise along the strokes.
- **Seed**: pseudo-random seed.
- **Randomize**: when enabled, the noise uses a random value over time. *Mode*: **Steps** (new value every *Step* frames) or **Keyframes** (new value only on keyframes).
- Influence filters: layer, layer pass, material, material pass, vertex group and a custom curve for the influence along each stroke.

## Recipes

- Line Art sketchiness: Line Art, then Noise on Position.
- Boiling outline: Randomize on with Mode Steps and a small Step value.

## Gotchas

- Noise is applied per point, so strokes with few points jitter coarsely; add points first (for example with a Subdivide modifier).
- Order matters: place Noise after generator modifiers (Line Art, Array) so it acts on their output.

## Verify

Play the timeline: with Randomize on, the noise changes at the chosen steps; with it off, the result is static.

## Checked

2026-10-27 against the Blender 5.2 manual (Grease Pencil Noise modifier page and modifier influence filters). Confirmed Position, Strength, Thickness, UV, Noise Scale, Noise Offset, Seed, Randomize Mode (Steps, Keyframes) and Step. Removed unconfirmed numeric recommendations, the frame rate claim, world-scale remarks and "Random toggle" wording.
Method: documentation only; no commands were run.
