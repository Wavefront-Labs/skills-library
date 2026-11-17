---
id: creative-arts.animation.texturing.painter-export-presets
name: painter-export-presets
category: creative-arts
field: animation
product: texturing
tags: [export-presets, texture-export, substance-painter, output-templates, naming-tokens, file-format, bit-depth, blender-export, arnold, unreal]
level: practitioner
status: draft
description: "Build Substance 3D Painter export presets per renderer/engine: output maps, naming tokens, formats and bit depth, padding, and a show-standard preset everyone uses."
sources:
  - https://helpx.adobe.com/substance-3d-painter/texturing/export/export-settings.html
  - https://helpx.adobe.com/substance-3d-painter/texturing/export/creating-export-presets.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Painter export presets

**Goal:** exported textures arrive with the names, channels, formats and bit depths the renderer and
pipeline expect, identical across artists.

## Anatomy of a preset (Export Textures - Output Templates)

- **Output maps**: each row is a file, e.g. `$mesh_$textureSet_BaseColor`, with RGB/A slots filled from
  Painter channels (Base colour, Roughness, Metallic, Normal, Height, AO, Emissive, Opacity, user
  channels, or converted maps like "Normal OpenGL", "Mixed AO").
- **Naming tokens**: `$mesh`, `$textureSet`, `$udim`, `$colorSpace` ... Use the pipeline's convention,
  e.g. `$textureSet_BaseColor.$udim`.
- **Format** per map: PNG/TIFF 8 or 16-bit, EXR 16/32 float. Colour maps 8-bit PNG/TIFF or 16-bit;
  height/displacement 16-bit or EXR (8-bit height steps visibly).
- **Padding**: dilation (infinite or N px) to avoid seams at mip levels.

## Typical presets

| Target | Maps |
|---|---|
| Blender Principled BSDF | BaseColor (sRGB), Roughness, Metallic, Normal (OpenGL), Height (16-bit), Emission |
| Arnold/aiStandardSurface | same, often 16-bit TIFF, tx conversion afterwards |
| Unreal | BaseColor, ORM packed (AO-Roughness-Metallic), Normal (DirectX) |
| Unity URP/HDRP | BaseMap, MaskMap packed (M, AO, detail, smoothness), Normal (OpenGL) |

Packing details: `creative-arts.animation.texturing.channel-packing-orm`.

## Making it standard

1. Duplicate the closest built-in template, edit, rename `SHOW_<renderer>_v01`.
2. Export the preset (it saves as a file in the shelf's export-presets folder) to the shared library.
3. Pair with the project template so every project defaults to it
   (`creative-arts.animation.texturing.painter-project-templates`).

## Gotchas

- Colour space: base colour and emission are sRGB; roughness, metallic, normal, height are linear
  data. The receiving shader must set them as Non-Color/Raw.
- Painter channels not present in a texture set export as empty or default values; check per set.
- Export "size" overrides can upscale beyond working resolution; procedural content recomputes, bitmaps
  do not.

## Verify

Export one asset, load it with the show's shader template in the renderer: maps connect by name without
manual work and the render matches Painter's viewport (allowing for lighting differences).
