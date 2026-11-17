---
id: creative-arts.animation.blender.white-balance
name: white-balance
category: creative-arts
field: animation
product: blender
tags: [blender, color-management, white-balance, white-point, temperature]
level: practitioner
status: docs-checked
description: "Use Color Management White Balance in Blender: temperature and tint, the colour picker on a neutral, Python ranges, and when to use the compositor or light colours instead."
sources:
  - https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
  - https://docs.blender.org/api/current/bpy.types.ColorManagedViewSettings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# white-balance

Goal: neutralise or warm/cool a whole render like a camera white balance.

## Render Properties > Color Management > White Balance

- Enable the checkbox (`use_white_balance`).
- **Temperature**: blackbody temperature of the primary illuminant; the default is a D65 white point (Python default 6500 K, range 1800 to 100000).
- **Tint**: green/magenta shift of the blackbody curve (Python default 10, which matches daylight; range -500 to 500).
- **Colour picker**: sample a colour that should be white; temperature and tint are set so it ends up balanced to white. The manual notes this only works if the colour is close enough to a blackbody emitter.

The manual says the adjustment makes a given white point end up as white on the display.

## When to use it

- Matching CG to a plate: pick a neutral from the render or set the plate's measured temperature.
- Light colour changes the light itself and its ratio with other lights; use it for creative colour differences between lights.
- The manual also points to the compositor's Color Balance node for white balancing as part of compositing, which keeps the correction visible in the node tree.

## Gotchas

- It is a view-level setting, so the Render Result and displayed images use it; check it is enabled in every scene you render.
- Files that skip the view (such as scene-linear EXR) do not carry it.

## Verify

Render a grey card, sample it with the picker, and check that its RGB values come out roughly equal.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/color_management/displays_views (White Balance: temperature, tint, colour picker, D65 default, works if the colour is close to a blackbody emitter; compositor alternative) and Python API ColorManagedViewSettings (use_white_balance, white_balance_temperature 1800..100000 default 6500, white_balance_tint -500..500 default 10). Removed unconfirmed version gate, processing-order and workflow claims.
Method: documentation only; no commands were run.
