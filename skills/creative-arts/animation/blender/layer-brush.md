---
id: creative-arts.animation.blender.layer-brush
name: layer-brush
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, layer-brush, persistent-base, height-limit, raised-detail]
level: practitioner
status: docs-checked
description: "Raise areas to an even height with Blender's Layer sculpt brush: Height, Persistent and Set Persistent Base, Hardness, for scars, plates and controlled relief."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/brushes/layer.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/brush_settings.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/texture.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# layer-brush

Goal: even-height relief that does not stack when strokes overlap: armour plates, raised scars, cloth seams, embossed designs.

## Settings

The Layer brush is a Draw-like brush type whose height is capped, which gives the appearance of a flat layer.

- **Height**: the fixed height of each stroke, measured in scene scale, so it stays consistent regardless of zoom or object size.
- **Persistent**: all strokes use the same height, as if sculpting a single layer. The manual recommends it, together with Set Persistent Base, so strokes do not add on top of each other.
- **Set Persistent Base**: resets the base so you can sculpt a new layer on top.
- **Hardness**: higher by default so the layer profile is more noticeable.

## Workflow

1. Enable Persistent and click Set Persistent Base on the clean surface.
2. Paint the design, going over areas repeatedly; the result is a uniform plateau.
3. Click Set Persistent Base again whenever the next layer should sit on top.
4. Tighten borders with the Pinch brush or soften them with Smooth.

## Use with masks and stencils

Use a mask for precise decals (mask outside, paint inside), or a texture with Stencil mapping on the brush (see `creative-arts.animation.blender.sculpt-texture-brush`).

## Gotchas

- Height is in scene units, so check Scene Units before choosing a value.
- Set Persistent Base again before starting each new layer, otherwise strokes keep the previous base height.

## Verify

Overlapping strokes produce a flat plateau under raking light (matcap), not stacked ridges.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/sculpting/brushes/layer: Height definition (scene scale), Persistent, Set Persistent Base, Hardness default, recommended persistent workflow. Removed unconfirmed claims about a Manual Normal option, Ctrl engraving, a sample Height value and base loss after remesh.
Method: documentation only; no commands were run.
