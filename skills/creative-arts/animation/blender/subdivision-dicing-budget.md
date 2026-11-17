---
id: creative-arts.animation.blender.subdivision-dicing-budget
name: subdivision-dicing-budget
category: creative-arts
field: animation
product: blender
tags: [blender, render-optimization, subdivision-render-levels, dicing-budget, adaptive-subdivision, subdivision-surface]
level: practitioner
status: docs-checked
description: "Control subdivision cost at render time: viewport vs render levels, Cycles adaptive subdivision dicing rate, offscreen scale, max subdivisions, dicing camera and Simplify caps."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/subdivision.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/simplify.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# subdivision-dicing-budget

Goal: smooth surfaces in renders without memory spikes or long sync times.

## Fixed levels (Subdivision Surface modifier)

- **Levels Viewport** and **Render**: the number of subdivision levels shown in the 3D Viewport or the final render. The manual warns against setting Viewport higher than Render, since the viewport would then look better than the render.
- Each level splits every face into four (quads), so face counts grow roughly four times per level. A 50k-face mesh at level 3 is about 3.2 million faces.
- Pick the render level where silhouettes stop showing facets at the final resolution; background props often need fewer levels.
- Simplify > Render > **Max Subdivision** caps subdivision levels everywhere for previews.
- Ctrl 1, Ctrl 2, Ctrl 3 add a Subdivision Surface modifier with that many Viewport levels and leave Render levels unchanged.

## Adaptive subdivision (Cycles only)

The modifier's **Adaptive Subdivision** option subdivides by distance to the camera, adding detail near and less far away, and is particularly useful for fine displacement detail. It has **Adaptive Space** (Pixel or Object) with **Pixel Size** or **Edge Length**.

Render Properties > **Subdivision** panel (Cycles):
- **Dicing Rate Render** and **Viewport**: multipliers for the size of micropolygons (final and viewport render).
- **Offscreen Scale**: multiplier for the dicing rate of geometry outside the camera view. Lower values give higher quality reflections and shadows for off-screen objects; higher values use less memory.
- **Max Subdivisions**: stop subdividing at this level even if the dicing rate would give finer tessellation.
- **Dicing Camera**: reference camera for subdividing, useful against crawling artefacts when the scene camera moves.

## Budgeting

- Watch render memory, and loosen the dicing rate before tightening it. Use a Dicing Camera when the camera moves, so dicing does not change frame to frame.

## Gotchas

- Instancing does not work well with Pixel space subdivision (it uses the original object's position); the manual recommends Object space for instanced meshes.
- Multi-view renders can show inconsistencies between views.

## Verify

Render a close and a far frame. Compare memory and silhouettes: edges should be smooth with no faceting and memory within your budget.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and the Cycles add-on source (ui.py on main).
Confirmed: Levels Viewport/Render wording and the viewport-above-render warning; Ctrl 1 shortcut behaviour; adaptive subdivision options and limitations; Subdivision panel settings and their definitions; Simplify Max Subdivision.
Removed as unconfirmed: the Experimental feature set requirement (the 5.2 Subdivision panel has no such condition), the per-object "Dicing Scale", the "dicing rate 1 is fine detail, 2 to 4 saves memory" guidance, "modifiers after Subdivision disable adaptive" and the per-instance dicing claim.
Method: documentation only; no commands were run.
