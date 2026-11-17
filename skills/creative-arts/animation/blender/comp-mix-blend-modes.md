---
id: creative-arts.animation.blender.comp-mix-blend-modes
name: comp-mix-blend-modes
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, mix-color-comp, mix-node-compositor, blend-modes]
level: practitioner
status: docs-checked
description: "Combine images with the compositor Mix Color node: Factor, A and B, blend modes, Clamp Factor and Clamp Result, mattes in Factor, and a Difference check."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/color/mix_color.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/color/mix.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# comp-mix-blend-modes

Goal: combine images with the right maths for the job.

## Mix Color node (Color category)

Inputs: **Factor**, **A** (base) and **B** (blend). Options: the blend mode, **Clamp Factor** (limit the factor to 0 to 1; if off the node extrapolates) and **Clamp Result** (limit the result to 0 to 1).

## Blend modes in the node

Add, Subtract, Multiply, Screen, Divide, Difference, Darken, Lighten, Overlay, Color Dodge, Color Burn, Hue, Saturation, Value, Color, Soft Light, Linear Light (plus Mix for a plain crossfade). Typical uses:

| Mode | Use |
|---|---|
| Mix | Crossfade, or replace through a matte in Factor |
| Add | Combining light passes, glows, light groups |
| Multiply | Colour passes times light passes, AO |
| Screen | Brightening without a hard sum |
| Overlay / Soft Light | Contrast layers |
| Difference | Checking two images match (black = identical); the manual's watermark example uses it |
| Subtract / Divide | Removing a pass |
| Darken / Lighten | Per-channel minimum and maximum |
| Hue / Saturation / Color / Value | Take that component from B |

## HDR data

Renders can hold values above 1. Leave **Clamp Result** off on light passes so highlights survive to the view transform, and test modes such as Screen and Overlay on a sample before trusting them with HDR input.

## Masks

Put a matte in Factor to apply B only in an area. This is the basic grade-through-a-matte move.

## Verify

Difference-mode check: Mix (Difference) a recombined image against Combined. The viewer should be black, with sampled values near 0.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: the node is named Mix Color, inputs Factor, A, B, the list of blend modes, Clamp Factor and Clamp Result, and the Difference-mode watermark check. Removed Use Alpha (not in 5.2) and the unconfirmed per-mode rules for scene-linear data.
Method: documentation only; no commands were run.
