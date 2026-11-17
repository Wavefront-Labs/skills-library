---
id: creative-arts.animation.blender.paint-brush-blend-modes
name: paint-brush-blend-modes
category: creative-arts
field: animation
product: blender
tags: [blender, texture-paint, paint-blend-modes, brush-blend-modes, accumulate, erase-alpha]
level: practitioner
status: docs-checked
description: "Pick texture-paint brush blend modes in Blender: Mix, Multiply, Overlay, Add, Erase and Add Alpha, Strength behaviour, stroke methods, and saving brush changes as assets."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/brush_settings.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/stroke.html
  - https://docs.blender.org/api/current/bpy.types.Brush.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# paint-brush-blend-modes

Goal: get the layered result you intend from a single paint pass instead of fighting opaque Mix strokes.

## Where
Texture Paint mode > Brush Settings > **Blend**. The setting sets how the colour or value is applied over the target Color Attribute, Vertex Group or Image Texture, so it is shared with Vertex Paint.

The Brush.blend list (Python API): Mix (default), Darken, Multiply, Color Burn, Linear Burn, Lighten, Screen, Color Dodge, Add, Overlay, Soft Light, Hard Light, Vivid Light, Linear Light, Pin Light, Difference, Exclusion, Subtract, Hue, Saturation, Color, Value, Erase Alpha, Add Alpha.

## Which mode for which job (practice)
| Job | Blend |
|---|---|
| Base colour blocking | Mix |
| Dirt or darkening | Multiply or Darken |
| Highlights or edge wear | Screen, Lighten or Add |
| Contrast glaze | Overlay or Soft Light |
| Hue shift keeping detail | Hue, Saturation or Color |
| Cut holes or an opacity mask | Erase Alpha |
| Restore erased alpha | Add Alpha |

**Add Alpha** makes the image more opaque where painted; **Erase Alpha** makes it transparent, revealing the checkerboard background (a tablet pen's eraser end toggles this mode). To see them in the Image Editor set Display Channels to Color & Alpha or Alpha.

## Build-up controls
- **Strength** is the maximum effect of each brush stroke for painting brushes; opacity never exceeds Strength however often the same surface is painted in one stroke. Shift F changes it interactively, F changes the size.
- **Stroke Method** (Alt E): Dots, Drag Dot, Space (dabs spaced by Spacing), Airbrush (continues while held, rate set by Rate), Anchored, Line, Curve. Dots apply on each mouse-move step, so a slower stroke accumulates more.
- Falloff shapes the stamp (see the brush Falloff page).

## Gotchas
- Blend modes act on the image in the active paint slot only.
- Erase Alpha needs an image with an alpha channel; save as a format with alpha such as PNG RGBA or OpenEXR.
- Changes to a brush asset's settings are temporary and discarded when Blender closes; keep them with **Save Changes to Asset**, or use **Duplicate Asset** to make a project-specific variant.

## Verify
Paint a Multiply stroke over a mid-grey area and over white: grey darkens while white shows the brush colour (expected from multiplication); the image shows `*` until saved.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): brush_settings.rst (Blend, Add/Erase Alpha, Display Channels tip, Strength, Shift F, F, brush asset Save Changes/Duplicate), stroke.rst (Stroke Method list, Alt E, Dots, Airbrush Rate), and the current Python API Brush.blend items. Removed: the Space-stroke accumulation sentence, the Ctrl invert claim, the 4.3+ version gate, the 0.5 grey neutral claim. Method: documentation only; no commands were run.
