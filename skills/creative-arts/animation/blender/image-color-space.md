---
id: creative-arts.animation.blender.image-color-space
name: image-color-space
category: creative-arts
field: animation
product: blender
tags: [blender, color-management, image-color-space, non-color, srgb-vs-linear, textures]
level: practitioner
status: verified
description: "Assign correct colour spaces to images: sRGB for colour maps, Non-Color for data maps, linear for EXR/HDR, and Save as Render vs raw data when saving images."
sources:
  - https://docs.blender.org/manual/en/latest/editors/image/image_settings.html
  - https://docs.blender.org/manual/en/latest/render/color_management/color_spaces.html
  - https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# image-color-space

Goal: textures load with the correct transfer function, and saved images contain what you expect.

## Input colour space

- The image **Color Space** setting says what space the file was saved in; Blender uses it to convert to its internal linear space.
- Blender automatically tries to guess the colour space; if wrong, set it in the image settings.
- Maps that store data rather than colour (normal and displacement maps, also when baking them) must be set to **Non-Color**.
- OpenEXR files are always stored in scene-linear colour spaces; the Linear entries (Linear Rec.709, Linear Rec.2020, ACEScg, ACES2065-1; Blender 4.5.14 also lists Linear CIE-XYZ D65 and E, Linear DCI-P3 D65 and Linear FilmLight E-Gamut, and has no Working Space entry) cover common EXR content.
- Colour maps (albedo, emission) normally use the colour space they were authored in, typically sRGB.

## Alpha (image settings)

API `Image.alpha_mode`: `STRAIGHT`, `PREMUL`, `CHANNEL_PACKED`, `NONE`. A new image in 4.5.14 is sRGB with Straight alpha.

**Straight** (separate RGB and alpha, common for PNG), **Premultiplied** (natural for renders and OpenEXR, represents emissive effects such as fire correctly), **Channel Packed** (different images packed in RGB and alpha, as game engines do), **None**.

## Saving

- **Save as Render** in the image save operator (`bpy.ops.image.save_as(save_as_render=True)`, or `Image.save_render()` in Python) applies the view, exposure, gamma and curves; it is meant for saving linear EXR to PNG/JPEG in display space.
- For data maps (normal, roughness) keep the Non-Color colour space and do not apply the view transform.

## Verify

Compare a test normal map set to sRGB versus Non-Color; only Non-Color should shade like the source.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) editors/image/image_settings (Color Space, Alpha options) and render/color_management (color_spaces: Non-Color, automatic guessing, OpenEXR note; displays_views: Save as Render). Removed unconfirmed texture-type table, Node Wrangler, library and Python claims.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Image.colorspace_settings.name items (ACES2065-1, ACEScg, AgX Base and Log spaces, Display P3, Filmic Log, Filmic sRGB, Khronos PBR Neutral sRGB, the Linear spaces named above, Non-Color, Rec.1886, Rec.2020, sRGB); alpha_mode items and defaults; image.save_as has save_as_render (default off); Image.save_render exists. Not run (confirmed from the manual only): automatic colour space guessing, the EXR-is-linear rule and the sRGB-versus-Non-Color normal map comparison.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
