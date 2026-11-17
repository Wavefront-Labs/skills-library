---
id: creative-arts.animation.blender.simplify-settings
name: simplify-settings
category: creative-arts
field: animation
product: blender
tags: [blender, render-optimization, simplify-settings, simplify-subdivision, texture-limit, simplify]
level: practitioner
status: docs-checked
description: "Use Render Properties > Simplify for fast previews and memory caps: max subdivision, child particles, texture limit, volume resolution, culling, separate viewport/render values."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/simplify.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# simplify-settings

Goal: global quality caps without editing every object.

## Render Properties > Simplify (tick the checkbox)

Separate **Viewport** and **Render** subpanels share these Common Settings:
- **Max Subdivision**: maximum number of subdivisions by Subdivision Surface modifiers.
- **Child Particles**: show only a subset of child hairs and particles (a fraction, so 0.1 means 10 percent).
- **Texture Resolution**: scale down image textures to reduce memory usage.
- **Texture Size Limit**: scale textures down so none is larger than the chosen size.

Viewport only:
- **Volume Resolution**: resolution percentage of volume objects in the viewport (mostly affects memory rather than computation time).
- **Normals**: skip computing custom normals and face corner normals when displaying meshes.

Also in the panel:
- **Culling** (Cycles): Camera Cull (with a Margin) and Distance Cull (with a Distance) remove objects automatically. See camera-distance-culling.
- **Grease Pencil**: Playback Only, Fill, Modifiers, Shader Effects, Layer Tinting and Anti-Aliasing toggles.

## Uses

- Animation playback: lower viewport Max Subdivision and Child Particles.
- Preview renders for lighting: Render subpanel with a Texture Size Limit and lower Max Subdivision. Untick Simplify for finals.
- Fitting a heavy shot on a smaller GPU: set a Render Texture Size Limit that suits the output resolution.

## Gotchas

- Simplify is per scene and saved in the .blend. A shot rendered with Simplify on by mistake gives soft or low-detail finals, so add a pre-render check (see qa-validation-script).
- The limits apply at render time and do not change the image files on disk.

## Verify

Toggle Simplify and compare render memory use and time, then check a 100 percent crop of the hero asset for quality loss.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: panel location, Common Settings, Viewport-only Volume Resolution and Normals, Culling, Grease Pencil options.
Removed as unconfirmed: the old name "Texture Limit" (now Texture Size Limit), example numeric values, and the statement that the texture limit is applied only at render time (kept only as the general note that files on disk are unchanged).
Method: documentation only; no commands were run.
