---
id: creative-arts.animation.blender.eevee-film-overscan
name: eevee-film-overscan
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, eevee-film, overscan, film-transparent, film]
level: practitioner
status: docs-checked
description: "Use EEVEE Film settings: filter size, transparent background for comp, and overscan to fix screen-space effects at frame edges."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/render_settings/film.html
  - https://docs.blender.org/api/current/bpy.types.SceneEEVEE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eevee-film-overscan

Goal: correct edges and alpha from EEVEE.

## Render Properties > Film

- **Filter Size**: pixel filter width. Pixel filters avoid aliasing by slightly blurring the image; lower values give crisper renders, higher values are softer and reduce aliasing.
- **Transparent**: renders the background transparent, for compositing the image over another background after rendering. Save in a format with alpha (for example PNG RGBA or OpenEXR); JPEG has no alpha.
- **Overscan** (with a size in percent): percentage of the render size added to the internal render buffer. It has a serious impact on performance but can fix render glitches around the perimeter of the image. The size range in the 5.2 properties is 0 to 50 percent. Per the API description it renders past the image border so screen-space effects do not disappear at the edge.

## When overscan matters

- Reflections, ray-traced lighting or Fast GI ambient occlusion disappearing at the frame edge as the camera pans (these are screen-space effects).
- Do not use Film Overscan to gain extra image for reframing or stabilising in post; it is internal only. Render a larger resolution and adjust the camera instead.

## Gotchas

- With Transparent on, check composites against a contrasting background to inspect alpha edges.
- Overscan cost grows with the added area; increase it only until the edge artifacts are gone.

## Verify

Render a pan with a glossy floor reaching the frame edge, with and without overscan. Reflections should stay solid up to the edge.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Film) and SceneEEVEE properties in the 5.2 source. Confirmed: Filter Size, Transparent, Overscan description and performance warning, overscan range. Removed unconfirmed: default filter size 1.5, world-still-lights-scene claim, premultiplied alpha note, glass-on-transparent behaviour, 3 to 10 percent rule of thumb, bloom mention.
Method: documentation only; no commands were run.
