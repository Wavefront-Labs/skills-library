---
id: creative-arts.animation.blender.bake-clear-image
name: bake-clear-image
category: creative-arts
field: animation
product: blender
tags: [blender, bake-clear-image, bake-image-setup, bake-target, texture-baking, cycles-bake, image-texture-node]
level: practitioner
status: docs-checked
description: "Set up bake target images in Cycles: new image size, bit depth and colour space, the active unconnected Image Texture node per material, Clear Image and saving results."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/baking.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/image.html
  - https://projects.blender.org/blender/blender/src/branch/blender-v5.2-release/source/blender/editors/object/object_bake_api.cc
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# bake-clear-image

Goal: every bake lands in the right image, with the right precision, and is not lost on save.

## Create the target image

Image Editor → *New* (or Shader Editor `Shift A → Texture → Image Texture → New`).
- Colour data (base colour, combined, diffuse): sRGB colour space.
- Data maps (normal, roughness, AO, displacement): Non-Color. The manual also tells you to use a 16-bit or 32-bit format (OpenEXR or TIFF) for displacement maps.

## Point the bake at it

Cycles bakes into the **active and selected Image Texture node** of each material on the object(s); a material without one is skipped:
1. In every material of the baked object, add an Image Texture node with the target image.
2. Select it so it is the active node. It does not need to be wired into the shader; it only marks the target.
3. Objects sharing one material share one active node; two materials on one object can point to the same image to bake into one atlas.

## Bake panel (Render Properties → Bake, Cycles only)

- *Output → Target: Image Textures*. *Clear Image* clears the image before baking; turn it off to accumulate bakes from several objects into one atlas.
- The bake uses the object's active UV map (Object Data → UV Maps); the bake operator also has a `uv_layer` option to override it.

## Save

Save the image from the Image Editor (Image → Save As) so the baked result is stored on disk.

## Gotchas

- Error `No active image found in material slot (N) for object "name"`: that material slot lacks the active Image Texture node (empty slots count too).
- Cycles bakes with the scene's render settings (samples, bounces), so match them to the quality you need.
- A data map tagged sRGB is interpreted with the wrong gamma when used; keep data maps Non-Color.

## Verify

After baking, the Image Editor shows content inside every UV island; save, reload the file and the image still has the bake.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Target Image Textures, Clear Image and the active-and-selected Image Texture requirement (baking page); active UV layer and uv_layer override and the "No active image found in material slot" message (object_bake_api.cc); 16/32-bit and Non-Color tip for displacement (Multiresolution page). Removed unsupported size/bit-depth table and the circular-dependency claim.

Method: documentation only; no commands were run.
