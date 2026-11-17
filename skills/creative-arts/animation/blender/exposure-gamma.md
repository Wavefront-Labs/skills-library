---
id: creative-arts.animation.blender.exposure-gamma
name: exposure-gamma
category: creative-arts
field: animation
product: blender
tags: [blender, color-management, exposure-gamma, exposure-control, gamma-control]
level: practitioner
status: docs-checked
description: "Use Color Management Exposure and Gamma correctly: stops-based exposure, why gamma is a last resort, what gets baked into saved files, and Cycles vs compositor exposure."
sources:
  - https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
  - https://docs.blender.org/api/current/bpy.types.ColorManagedViewSettings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# exposure-gamma

Goal: set the overall brightness the right way without breaking lighting ratios.

## Render Properties > Color Management

- **Exposure** (stops): `output = render_value x 2^exposure`, applied before the colour space conversion. +1 doubles brightness, -1 halves it. Python range -32 to 32, default 0.
- **Gamma**: extra gamma correction applied after the colour space conversion. The default display transforms already do the appropriate conversion, so the manual says it mainly acts as an additional artistic effect. Python range 0 to 5, default 1.0.

## What gets applied where

- Render Result, Viewer and files saved by Render Animation have the render view applied.
- Other images (such as an intermediate EXR) need **View as Render** to display with view, exposure, gamma and curves, and **Save as Render** in the save operator to write them to PNG/JPEG in display space.
- OpenEXR files are always stored in scene-linear colour spaces, so a compositor reading an EXR sees the linear values.

## Practical notes

- Fix lighting first, then use Exposure for the overall level; extreme exposure changes amplify noise in dark scenes (a general rendering consideration, not a manual claim).
- Leave Gamma at 1.0 unless you want an artistic effect.

## Verify

Sample the brightest important surface with the Image Editor's sample tool and confirm it is in the expected range for the view transform.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/color_management/displays_views (Exposure formula and stage, Gamma, View as Render, Save as Render, EXR note) and Python API ColorManagedViewSettings (exposure range -32..32, gamma 0..5). Removed unconfirmed practical-use, multi-scene and VSE claims.
Method: documentation only; no commands were run.
