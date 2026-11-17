---
id: creative-arts.animation.texturing.painter-fill-layers
name: painter-fill-layers
category: creative-arts
field: animation
product: texturing
tags: [fill-layers, painter-layers, layer-stack, substance-painter, paint-layers, blending-modes, channel-toggles, folders, non-destructive]
level: practitioner
status: draft
description: "Structure Substance 3D Painter layer stacks with fill and paint layers: channel toggles, blending per channel, folders with masks, and a stack order that stays editable."
sources:
  - https://helpx.adobe.com/substance-3d-painter/interface/layer-stack.html
  - https://helpx.adobe.com/substance-3d-painter/interface/layer-stack/creating-layers-and-folders.html
  - https://helpx.adobe.com/substance-3d-painter/painting/fill-projections.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fill layers and paint layers

**Goal:** a layer stack that reads like the material: base material, variation, wear, dirt, details,
each editable later.

## Layer types

| Type | Content | Use |
|---|---|---|
| Fill layer | uniform values or a material/texture per channel, projected (UV, tri-planar, planar) | most material work: base metal, paint, rust colour |
| Paint layer | brush strokes | hand-painted details, touch-ups |
| Folder | groups layers; can carry a mask | a "paint over metal" material group |

A fill layer + a mask is the core move: the material lives in the fill, where it shows lives in the mask.

## Channels and blending

- Each layer has per-channel toggles (Base colour, Roughness, Metallic, Height, Normal...). Turn off
  channels a layer should not touch (a dirt layer usually affects colour and roughness, not metallic).
- Per-channel blend modes and opacity (click the blend mode next to each channel): Height usually
  Normal or Add, Normal channel "Normal map combine" for detail normals.

## Recommended stack order (bottom to top)

1. Base material fill (folder "Base").
2. Colour/roughness variation fills with grunge masks (large to small scale).
3. Edge wear and scratches (folder with smart mask).
4. Dirt, dust, stains (folders with AO/cavity masks).
5. Decals, labels, hand-painted details (paint/projection layers).
6. Final adjustments (filter layers: HSL, levels on colour only).

Name every layer and folder; colour-code folders by stage.

## Gotchas

- Painting directly on a fill's colour is not possible: paint in its mask, or use a paint layer.
- Too many full-resolution paint layers make projects heavy; fills with procedural masks are lighter.
- Height and Normal channels: do not stack strong height and a baked normal that already has the same
  detail (double-detail look).

## Verify

Toggle each folder off and on: each changes only what its name says; channel viewer (C key cycles
channels) shows roughness and metallic behaving as intended per layer.
