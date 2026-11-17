---
id: creative-arts.animation.blender.paint-stencil-texture-mask
name: paint-stencil-texture-mask
category: creative-arts
field: animation
product: blender
tags: [blender, texture-paint, stencil-mapping, texture-mask, stencil-texture, brush-texture]
level: practitioner
status: docs-checked
description: "Stamp photos and decals with Blender texture-paint stencils: Stencil mapping, RMB move/scale/rotate keys, Image Aspect, Texture Mask, Pressure Masking and overlay opacity."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/texture.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/cursor.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# paint-stencil-texture-mask

Goal: project a reference image (decal, photo, pattern) through a screen-space stencil onto a model.

## Setup
1. Brush Settings > **Texture**: assign an image (or procedural) texture.
2. **Mapping: Stencil**. Stencil mapping projects the texture from camera space onto the mesh or canvas; painting is applied only inside the stencil boundaries, and the stencil is shown as a screen-space overlay. The manual calls it the ideal option for stamping textures for projection painting.

## Moving the stencil (default keymap)
| Action | Keys |
|---|---|
| Move | RMB drag |
| Scale | Shift RMB drag |
| Rotate | Ctrl RMB drag |
| Same for the Texture **Mask** stencil | hold Alt |
While scaling, X and Y constrain to one axis (press again for unconstrained). **Image Aspect** restores the original image aspect ratio to undo stretching from scaling (image textures only). **Reset Transform** restores the stencil position.

## Texture Mask
The Texture Mask panel offers the same settings as Texture and controls the strength of the brush, for example a soft grunge so a hard decal fades at the edges. **Pressure Masking** (Texture Mask only): Off, **Ramp** fades the mask effect on higher pressure, **Cutoff** expands the used image values by stylus pressure. 3D mapping is not available for the Texture Mask.

## Other mappings
View Plane (current view angle, good for projection painting), Area Plane (along the local surface normal, avoids stretching on steep angles; the manual's recommended default), Tiled, 3D (procedural textures, using vertex coordinates), Random (random texture coordinate for each stroke step).

## Gotchas
- A stencil projects along the view, so paint from a view square to the surface or it stretches over grazing faces (practice). Area Plane avoids stretching on steep angles.
- Overlay opacity is set in the brush **Cursor** settings (Texture Overlay Alpha); a hidden overlay does not mean the stencil is off.
- Colour space: photos sRGB, masks Non-Color (practice).

## Verify
Paint one sweep across the stencil: the decal lands undistorted where the surface faces the view and fades where the mask is dark.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): sculpt_paint/brush/texture.rst (Mapping types, Stencil description and keys including Alt for mask, X/Y constraint, Image Aspect, Reset Transform, Pressure Masking, 3D not available for mask) and brush/cursor.rst (texture overlay alpha). Removed: the Options > Normal falloff claim (not in the Options panel), the "brush colour x texture" colour rule, and the Blend Mix/Multiply guidance. Method: documentation only; no commands were run.
