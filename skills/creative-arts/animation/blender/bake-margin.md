---
id: creative-arts.animation.blender.bake-margin
name: bake-margin
category: creative-arts
field: animation
product: blender
tags: [blender, bake-margin, margin-type, texture-baking, bake-padding, mipmap-seams]
level: practitioner
status: verified
description: "Control bake padding in Cycles: margin size in pixels, Adjacent Faces versus Extend margin types, resolution and mipmap rules, and fixing visible UV seams."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/baking.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/intern/cycles/blender/addon/ui.py
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/editors/object/object_bake_api.cc
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# bake-margin

Goal: no visible seams on UV borders when the texture is filtered or mip-mapped in an engine.

## Settings (Render Properties → Bake → Output → Margin)

When baking to images a margin is generated around UV islands by default; it avoids discontinuities at UV seams caused by texture filtering and mip-mapping.

- **Type**:
  - *Extend*: extends border pixels outwards.
  - *Adjacent Faces*: fills the margin using pixels from adjacent faces across UV seams.
- **Size**: margin size in pixels.

The Margin panel only appears for the *Image Textures* target (not for *Active Color Attribute*). For Tangent-space Normal bakes and UV bakes only *Size* is shown, without *Type*.

## Scripting

`bpy.ops.object.bake` exposes `margin` (default 16) and `margin_type` (default `EXTEND`) as operator options; the panel values are scene settings (`scene.render.bake.margin`, 16, and `scene.render.bake.margin_type`, an enum of `ADJACENT_FACES` and `EXTEND`). In 4.5.14 factory settings the scene `margin_type` reads `ADJACENT_FACES` while the operator argument default is `EXTEND`, so set `margin_type` explicitly in scripts.

## Verify

View the baked texture at a distance (or with mipmaps in the engine): no dark or coloured lines along seams; in the Image Editor zoom to an island edge and see the dilated colour band of the chosen width.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Margin Type (Extend, Adjacent Faces) and Size, purpose of the margin (baking page); panel visibility rules (ui.py); operator margin and margin_type defaults (object_bake_api.cc). Removed the unsupported "Adjacent Faces is default" claim, the margin-by-resolution table and the island spacing rule.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): bpy.ops.object.bake properties margin=16, margin_type=EXTEND (ADJACENT_FACES or EXTEND), target IMAGE_TEXTURES or VERTEX_COLORS; scene.render.bake margin 16 and margin_type ADJACENT_FACES in factory settings. Not run (confirmed from the manual only): the panel visibility rules and the seam appearance.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
