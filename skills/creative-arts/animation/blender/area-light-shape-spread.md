---
id: creative-arts.animation.blender.area-light-shape-spread
name: area-light-shape-spread
category: creative-arts
field: animation
product: blender
tags: [blender, lights, area-light, area-light-shape, area-light-spread, area-light-size, softbox]
level: practitioner
status: docs-checked
description: "Use Blender area lights: square, rectangle, disk and ellipse shapes, size for softness and Spread to focus the beam like a softbox grid."
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://docs.blender.org/manual/en/latest/render/cycles/light_settings.html
  - https://docs.blender.org/api/current/bpy.types.AreaLight.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/makesrna/intern/rna_light.cc
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# area-light-shape-spread

## Settings

- **Shape**: Square, Rectangle (Size X / Size Y), Disk, Ellipse. Square and Disk use *Size*; Rectangle and Ellipse use X and Y.
- **Size**: the light's dimensions. The area light produces soft shadow borders by sampling a light across a grid of the size you set; a larger size gives softer shadows.
- **Spread** (Cycles, Light → Beam Shape): how wide the emitted light fans out, range 0 to 180 degrees. Larger values give softer shadows; smaller values give sharper light simulating a gridded softbox. The 5.2 EEVEE light panel has no Spread setting.
- **Portal** (Cycles, Light → Settings): turns the area light into a light portal (see `creative-arts.animation.blender.light-portals`).
- **Normalize**: by default the total power stays the same when the size or shape changes; turn it off to emit more light as the light gets bigger.

```python
import bpy, math
a = bpy.data.lights.new("Softbox", 'AREA'); a.shape = 'RECTANGLE'
a.size, a.size_y = 1.0, 1.4; a.spread = math.radians(45); a.energy = 300
```

## Gotchas

- Lights are not directly visible in the rendered image; use an emissive mesh if the source should appear in camera.
- Choose the shape to match the source: a rectangle for a window or neon tube, a square for a TV screen (manual tip).

## Verify

Shadows soften as size increases; in Cycles a narrower Spread gives a more focused beam.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Shapes and Size/Size X/Size Y, Normalize, shape tip (Light Objects page); Spread meaning and Portal (Cycles light settings page); Spread 0-180 degree range, Spread only in the Cycles Beam Shape panel and size/size_y/spread property names (rna_light.cc, ui.py, properties_data_light.py). Removed unsupported claims (emission side, example sizes, scale behaviour, noise).

Method: documentation only; no commands were run.
