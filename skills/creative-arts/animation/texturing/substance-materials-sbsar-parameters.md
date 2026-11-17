---
id: creative-arts.animation.texturing.substance-materials-sbsar-parameters
name: substance-materials-sbsar-parameters
category: creative-arts
field: animation
product: texturing
tags: [sbsar, substance-materials, procedural-materials, painter, parameters, substance-engine, texturing]
level: practitioner
status: draft
description: "Use Substance (sbsar) procedural materials in Painter and pipelines: exposed parameters, resolution and seed, baking to bitmaps, and the sbsrender command line."
sources:
  - https://helpx.adobe.com/substance-3d-painter
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Substance materials (sbsar) parameters

An **sbsar** is a published Substance archive: a procedural material, filter or generator authored in Substance 3D Designer (or downloaded from Substance 3D Assets or Sampler). It generates its texture maps from **exposed parameters** instead of storing fixed bitmaps.

## In Painter
1. Import the sbsar into the project (Import resources) and drag the material onto a fill layer or use it as a smart-material component, or apply a filter or generator layer.
2. The **Properties panel** shows the sbsar's published parameters, for example scale, colour variations, roughness, wear amount and a random seed. Different archives expose different parameters, and the author chooses which.
3. Output maps feed the layer's channels (base colour, roughness, metallic, normal, height).
4. Adjust per layer; combine with masks and generators like any material (`painter-fill-layers.md`).

## Parameters you will meet
- **Output size** (power-of-two resolution) and a **random seed** to vary the pattern.
- **Scale/tiling**, **rotation**, **colour** or **hue** shifts, and "wear/dirt/moss" amounts.
- Parameters change the result **procedurally**, so changes are cheap and resolution-independent.

## Outside Painter
- Adobe's Substance Automation Toolkit includes `sbsrender`, a command-line tool to render sbsar to bitmaps; options such as `--set-value` set parameters. Check the toolkit's documentation for exact syntax and licensing.
- Game engines (Unreal, Unity) use the Substance plug-ins to evaluate sbsar at runtime or bake to textures. Offline-bake for animation renders so the scene does not depend on the plug-in.

## Practice
- Record the sbsar file name, version and parameter values with the asset so you can reproduce it (`painter-project-templates.md`).
- Bake to bitmaps for hand-off, with the export preset (`painter-export-presets.md`).

## Verify
- [ ] Parameters stored with the project or in the asset notes.
- [ ] Baked maps match the viewport, at the right resolution.
