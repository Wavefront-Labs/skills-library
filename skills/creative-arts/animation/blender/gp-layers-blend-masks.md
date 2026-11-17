---
id: creative-arts.animation.blender.gp-layers-blend-masks
name: gp-layers-blend-masks
category: creative-arts
field: animation
product: blender
tags: [blender, grease-pencil, gp-layers-blend, gp-layer-masks, gp-layer-opacity, gp-layers]
level: practitioner
status: docs-checked
description: "Organise Grease Pencil drawings with layer groups, blend modes, opacity, masks with invert, lights, adjustments and per-layer relations."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/properties/layers.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/properties/strokes.html
  - https://docs.blender.org/api/current/bpy.types.GreasePencilLayer.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gp-layers-blend-masks

Goal: line, colour and shading on separate layers that composite like a 2D app.

## Layer tree (Object Data > Layers)
Layers sit in a tree; **Layer Groups** (Add New Layer Group, drag and drop, colour tag) fold related layers. Default view order is top to bottom. Row icons: Use Mask, Onion Skinning, Hide, Lock. Layer Specials: Duplicate, Duplicate Empty Keyframes, Show All, Hide Others, Lock All, Unlock All, Autolock Inactive Layer, Ignore Material Locking, Merge Down (Shift-Ctrl-M), Merge Group, Merge All, Mask with Layer Above/Below, Copy Layer to Selected. Layer groups cannot be added from the Dope Sheet.

## Per-layer settings
- **Blend Mode**: Regular, Hard Light, Add, Subtract, Multiply, Divide.
- **Opacity**.
- **Lights**: layer is affected by scene lights when enabled (Python: use_lights, default False).
- Adjustments: Tint Color, Factor, Stroke Thickness override.
- Relations: Parent, Pass Index, View Layer, Use Masks in Render.

## Masks
There are no special mask layers: any layer can mask another. In the Masks panel add the layers that mask the current one; each entry has Invert and Hide. Mask layers keep their own blend mode and opacity; for a fully transparent mask set the mask layer's opacity to 0. The Use Mask icon or panel checkbox toggles the effect.

## Gotchas
- Fade Inactive Layers (overlay) reduces distraction from layers you are not editing.
- Stroke Depth Order (Object Data > Settings) decides whether layer order (2D Layers) or real 3D position drives draw order.
- Use Masks in Render off removes masks from view-layer renders.

## Verify
Toggle a mask's Invert: the masked layer flips between showing inside and outside the mask shape.

## Checked

2026-10-27, Blender 5.2 manual (projects.blender.org blender-manual, branch blender-v5.2-release RST) and Python API docs. Confirmed layer tree icons and specials, Masks panel (no special mask layers, Invert, Hide), Lights, Adjustments and Relations, Stroke Depth Order, and the six blend mode enum values via GreasePencilLayer.blend_mode. Removed the shadow and glow recipe advice, the transparent-film Multiply claim and the 4.3 version gate.
Method: documentation only; no commands were run.
