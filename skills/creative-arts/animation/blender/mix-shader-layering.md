---
id: creative-arts.animation.blender.mix-shader-layering
name: mix-shader-layering
category: creative-arts
field: animation
product: blender
tags: [blender, shader, shader-nodes, mix-shader-layering, mix-shader, add-shader, layered-material]
level: practitioner
status: docs-checked
description: "Layer Blender materials with Mix Shader and Add Shader: masks from textures, Layer Weight, energy conservation, and when to mix Principled inputs instead."
sources:
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/mix.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/add.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/ao.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/bevel.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/geometry.html
  - https://docs.blender.org/manual/en/5.2/render/shader_nodes/input/layer_weight.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mix-shader-layering

## Mix Shader

- Mixes two shaders so incoming rays hit either one with the probability given by **Factor**: 0 uses the first shader entirely, 1 the second. Layering example: a glossy and a diffuse shader make a ceramic material. A Layer Weight (Blend Weight) output is a typical Factor source.
- Factor from a mask (image, noise, vertex colour, AO) blends two complete materials, for example rust and paint or dirt and clean.

## Add Shader

Adds two shaders together. Use it for combinations such as emission added to a surface; for two BSDFs prefer Mix Shader.

## Alternative: mix inputs, not shaders

For two PBR materials you can mix their Base Color, Roughness and Normal with Mix (Color) or Map Range and feed one Principled BSDF.

## Mask building

- Edge wear: Geometry Pointiness (Cycles only) or the Bevel or AO node (Cycles only) -> Color Ramp -> Factor.
- Dirt in crevices: AO node (Inside off) -> Color Ramp.
- Height-based: Separate XYZ of Object coordinates Z -> Map Range.
- Noise breakup: multiply a mask by noise (Mix Color Multiply), then a Color Ramp to sharpen.

## Verify

Set the Factor to 0 and 1 in turn (or preview the mask through an Emission shader): each layer looks right alone and the mask is placed where expected.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch, docs.blender.org manual en/5.2). Confirmed against shader/mix (probabilistic Factor, 0 = first and 1 = second shader, Blend Weight example), shader/add, input/ao, input/bevel, input/geometry (Pointiness Cycles only) and input/layer_weight. Removed the unconfirmed 'energy conserving' wording, the performance and bakeability claims, the EEVEE cost gotcha, the Non-Color Factor remark and the Node Wrangler preview shortcut.

Method: documentation only; no commands were run.
