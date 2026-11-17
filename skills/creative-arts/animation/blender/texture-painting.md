---
id: creative-arts.animation.blender.texture-painting
name: texture-painting
category: creative-arts
field: animation
product: blender
tags: [blender, texture-paint, texture-painting, image-paint, stencil-paint, projection-paint, clone-brush, paint-slots, image-editor, brush-masks, hand-painted-textures, bleed, seams]
level: advanced
status: docs-checked
description: "Paint textures on meshes in Blender: paint slots, brush types, stencil and clone projection, seam bleed, saving images, known limitations."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/introduction.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/brushes.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/tool_settings/texture_slots.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/tool_settings/options.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/texture.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/editing.html
licence: Apache-2.0
version: 6
updated: 2026-11-17
aliases: []
---

# texture-painting

Goal: hand-paint colour, masks and data maps on a UV'd mesh inside Blender, with projection tools for photo detail, and get the result saved.

## Setup

1. The mesh must be unwrapped (`creative-arts.animation.blender.uv-unwrapping`). With no UV layer Blender shows a warning; in Texture Paint mode *Add Simple UVs* does a cube unwrap plus pack (available only when the object has no UV map), but a custom unwrap is still recommended.
2. Start painting in any of three ways: use the Texture Paint workspace (3D Viewport in Texture Paint Mode, Image Editor in Paint mode); choose Texture Paint Mode in the 3D Viewport header; or switch the Image Editor to Paint mode. Changes in either editor show immediately in the other.
3. **Texture Slots** (tool settings): the combination of images and UV maps. Mode *Material* detects slots from the mesh's materials (for Cycles, every Image Texture node in the node tree is listed; click a slot in the list to make it active). Mode *Single Image* paints one chosen image (with *New* to create one) on the chosen UV map, with a Linear or Closest texture filter; it does not touch the material.
4. Speed: Texture Paint is fast in the 3D Viewport when the image is square with power-of-two sides (256, 512, 1024...).
5. To preview the result in context, put a 3D Viewport in *Texture* shading beside an Image Editor holding the image.

## Brush types

- **Draw** (the normal brush; Essentials brushes include Paint Hard/Soft, Erase and Pixel Art variants - Pixel Art is Image Editor only).
- **Soften**: blur (Gaussian or Box blur mode) or Sharpen (with Sharp Threshold); *Kernel Radius* is 2D only.
- **Smear**: takes the colours under the cursor and blends them along your stroke.
- **Clone**: copies colours from another image or from another location of the same image. In 3D projective painting set the clone cursor with `Ctrl-LMB`; in 2D drag the clone with `RMB`. *Clone from Paint Slot* (3D projective only) uses another image as the source, chosen in *Source Clone Slot*.
- **Fill**: fills adjacent pixels of similar colour (*Fill Threshold*, 2D only); with the Gradient colour picker, drag to define a Linear or Radial gradient. In projective painting Fill bypasses the occlude, backface and normal-cull options.
- **Mask**: paints grayscale values on the mask texture; masked areas are not affected by other brushes. *Mask Value* 0 is unmasked and 1 fully masked; hold `Ctrl` to invert. The manual also offers face selection masking as a simpler alternative.
- `Shift-X` samples a colour into the active Paint brush; `Shift-Ctrl-X` samples the merged viewport colour including lighting, shading and visible layers.

## Brush textures and stencils

A brush **Texture** supplies colour in paint modes; a **Texture Mask** controls brush strength. Mapping options: View Plane (current view angle, good for projection painting), Area Plane (along the surface normal, avoids stretching on steep angles; the manual's suggested default), Tiled, 3D (procedural textures, not available for Texture Mask), Random, and **Stencil**.

Stencil mapping projects the texture from camera space and paints only inside the stencil boundary, shown as a screen-space overlay. Move with `RMB`, scale with `Shift-RMB`, rotate with `Ctrl-RMB` (hold `Alt` for the Texture Mask); `X` / `Y` constrain scaling to one axis. *Reset Transform* restores the stencil position and *Image Aspect* restores the image's aspect ratio. *Pressure Masking* (Texture Mask only) has Off, Ramp and Cutoff modes. *Angle* (`Ctrl-F`) rotates the texture; *Rake* (angle follows the stroke) and *Random* angle are not available with 3D, Tiled or Stencil mapping.

## Options and external editing

- **Bleed** extends paint beyond UV island bounds to avoid seam artefacts; **Dither** applies when painting on 8-bit images; **Occlude** limits painting to exposed pixels (and allows 3D stencils to mask areas); **Backface Culling** restricts painting to front faces.
- **External**: *Quick Edit* sends a snapshot of the viewport to an external image editor (size set by *Screen Grab Size*), *Apply* projects the edited image back onto the object, and *Apply Camera Image* projects an edited render from the active camera.
- You can also edit the image in any external paint program (GIMP, Krita) and reload it in the Image Editor.

## Saving images

The painted image is **not saved automatically**. An asterisk on the Image menu means it has changed but is unsaved. Use *Save Image* / *Save Image As*, or *Save All Images* in the Texture Slots panel (repacks, or saves an external file, for all edited images). Saving defaults to PNG and the format is independent of the render format. If the image is packed (File Browser Packing option or a manual pack), saving to a separate file is not necessary. Keep UV textures in a directory separate from other images.

## Known limitations

- Overlapping UVs are generally not supported; a problem when one brush stroke paints several faces that share texture.
- In perspective view a face partially behind the view cannot be painted: zoom out or use an orthographic view.
- On low-poly objects with normals pointing away from the view (the side of a cube) painting may fail; disable *Normal Falloff* in the stroke settings.
- A mesh can have several UV textures, but each UV texture has only one image.

## Verify

- The Image Editor shows your strokes and the asterisk is gone after saving; reopening the file shows the texture.
- Zoom into a seam on the model: no visible line (Bleed doing its job).
- The intended slot or image is active before painting (activating a slot also shows its image in the Image Editor).

See also `creative-arts.animation.texturing.texture-painting` (`../texturing/texture-painting.md`) for the cel-pipeline-specific use of Texture Paint.

## Checked

2026-11-09. Confirmed against the Blender manual Texture Paint Introduction, Brushes, Texture Slots, Options and Editing pages and the brush Texture & Texture Mask page (raw RST, all read in full). The Texture Paint Masking page and the brush Stroke and Brush Settings pages were not read, so related claims were removed: slot `+` presets and Principled wiring, 32-bit float and generated types, shortcuts `F` / `Shift F`, blend-mode list, stroke methods and stabilisation, falloff list, cavity mask, symmetry and tiling, 4K/8K performance figures, undo memory, colour-space and mirror gotchas, PNG 16-bit/EXR advice and the fake-layers recipe (the page says only that each UV texture has one image).
Method: documentation only; no commands were run.
