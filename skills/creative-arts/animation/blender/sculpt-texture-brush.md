---
id: creative-arts.animation.blender.sculpt-texture-brush
name: sculpt-texture-brush
category: creative-arts
field: animation
product: blender
tags: [blender, sculpting, sculpt-texture-brush, alpha-brush, brush-texture, stencil, skin-pores, surface-detail]
level: practitioner
status: docs-checked
description: "Sculpt pores, scales and fabric with texture brushes in Blender: mapping modes (view, area, tiled, 3D, random, stencil), angle, sample bias and texture masks."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/texture.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/stroke.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# sculpt-texture-brush

Goal: high-frequency surface detail from grayscale textures, applied cleanly without tiling artefacts.

## Setup

1. In Sculpt Mode, open the brush's Texture panel and assign any image or procedural texture (load images as image textures first, then pick them from the data-block menu). In sculpting the texture determines the strength of the brush.
2. Choose **Mapping** (also set per texture mask as Mask Mapping). The manual recommends Area Plane or View Plane for the usual behaviour and matching it with the Sculpt Plane setting:
   - *View Plane*: projects the texture along the viewing angle.
   - *Area Plane*: projects along the local surface normal, avoiding stretching on steep angles; a good default for most brushes.
   - *Tiled*: repeats the texture across the screen, so moving the brush does not change where the texture lands; best with tileable images.
   - *3D*: uses vertex coordinates, suited to procedural textures; not available for the Texture Mask.
   - *Random*: picks a random texture coordinate for each step of the stroke.
   - *Stencil*: projects the texture from camera space and affects only the area inside the stencil, shown as a screen overlay. RMB moves it, Shift-RMB scales (X or Y constrains the axis), Ctrl-RMB rotates; hold Alt for the Texture Mask. **Image Aspect** and **Reset Transform** fix a stretched or moved stencil.
3. **Angle** (Ctrl-F interactive) sets the rotation. **Rake** makes the angle follow the stroke direction; **Random** randomizes it per step with a **Random Angle** range. Neither is available with 3D, Tiled or Stencil mapping.
4. **Offset** and **Size** (X, Y, Z) place and scale the texture. **Sample Bias** (Sculpt Mode) adds a value to the samples, for height maps whose mid-level is wrong. **Vector Displacement** (Sculpt Mode) uses colour channels to displace in three directions, supported only for the Draw brush with Area Plane mapping.
5. Stroke methods such as Drag Dot or Anchored (Stroke panel) stamp a single texture.

## Texture Mask

The Texture Mask panel has the same settings but controls the brush strength with a second texture (for example noise breakup). **Pressure Masking** (Off, Ramp, Cutoff) is available only for the mask.

## Gotchas

- The Rake and Random angle shortcuts are not available in Sculpt Mode; set them in the Texture panel.
- Stencil transforms act on the texture (hold Alt for the Texture Mask), not on the mesh.

## Verify

Under raking-light matcap shading the detail reads at the intended distance without visible tiling or stamp borders.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against sculpt_paint/brush/texture and stroke: mapping modes (Random picks random coordinates, not per-dab rotation; 3D is a mode), stencil keys and Alt for mask, Image Aspect, Reset Transform, Ctrl-F angle, Rake and Random availability, Sample Bias, Vector Displacement limits, Pressure Masking. Removed unconfirmed claims: 16-bit alpha advice, Extension Clip and Repeat, the skin pore recipe numbers and the 100 percent spacing trail.
Method: documentation only; no commands were run.
