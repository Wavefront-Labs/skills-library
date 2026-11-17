---
id: creative-arts.animation.blender.image-save-pack
name: image-save-pack
category: creative-arts
field: animation
product: blender
tags: [blender, texture-paint, image-save-pack, save-all-images, pack-images, unsaved-images]
level: practitioner
status: docs-checked
description: "Never lose painted textures in Blender: Save, Save All Images, Pack, Save Modified Images preference, formats and bit depth for painted maps, and checking unsaved images."
sources:
  - https://docs.blender.org/manual/en/latest/editors/image/editing.html
  - https://docs.blender.org/manual/en/latest/files/blend/packed_data.html
  - https://docs.blender.org/manual/en/latest/files/media/image_formats.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# image-save-pack

Goal: painted images persist with the file and in the format downstream tools expect.

## Painted images are separate data
Images edited in Blender (painted textures, generated images, compositor results) are stored separately from the .blend. Whether saving the .blend also saves modified images depends on the **Save Modified Images** preference (ask, save automatically, or ignore). Unsaved images are marked with an asterisk in the Image Editor. Render Result and Viewer node images are temporary and are never saved for you.

## Save
- Image Editor > Image > **Save** (Alt S), **Save As** (Shift Alt S) for a format change.
- **Image > Save All Images** saves every modified image; packed images are repacked.
- The Image menu entry shows `*` for modified images; Outliner Blender File view lists images.

## Format choice
| Use | Format |
|---|---|
| Colour maps for web or engines | PNG 8-bit RGB(A) |
| Roughness, metal, masks | PNG 8 or 16-bit, image colour space Non-Color |
| Height, displacement, anything needing float | 16-bit PNG, or OpenEXR half/float |
| Maps with Erase Alpha | RGBA PNG or EXR (JPEG has no alpha) |

PNG supports 8 and 16 bit, JPEG is 8 bit with no alpha, OpenEXR stores float 16 or 32 bit. Save images with float precision as OpenEXR (or Radiance HDR). Colour-space and format choices are practice.

## Pack
- Image > **Pack** (single image) or File > External Data > **Pack Resources** (all). Packing happens on the next save of the .blend.
- File > External Data > **Automatically Pack Resources** marks all eligible external files as packed, including ones added later.
- **Unpack Resources** offers "Use files in current directory (create when necessary)" (writes into folders such as `textures` next to the .blend, reusing a file that already exists) and "Write files to current directory (overwrite existing files)".

## Gotchas
- Saving as JPEG is lossy and discards alpha; avoid round-tripping paint through JPEG.
- A packed image is saved inside the .blend; the original external file is not updated.

## Verify
Save, close and reopen the .blend: painted detail is still there and no image shows `*`.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): files/media/image_formats.rst (Saving Modified Images, preference, asterisk, format channel depth and alpha table, Float Half/Full for OpenEXR), editors/image/editing.rst (Save Alt S, Save As Shift Alt S, Save All Images repacks packed images, Image > Pack), files/blend/packed_data.rst (Pack Resources, Automatically Pack Resources, Unpack options). Removed: Report Missing Files, Make Paths Relative, per-tile UDIM save claim and the "Ctrl S alone does not save images" claim (behaviour is preference-dependent). Method: documentation only; no commands were run.
