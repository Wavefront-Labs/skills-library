---
id: creative-arts.animation.blender.png-jpeg-tiff-settings
name: png-jpeg-tiff-settings
category: creative-arts
field: animation
product: blender
tags: [blender, output-settings, png-jpeg-settings, color-depth, png-compression, file-format]
level: practitioner
status: docs-checked
description: "Pick image output settings: PNG, JPEG, TIFF, OpenEXR and others, BW/RGB/RGBA, color depth, compression and quality, and the color management override on save."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
  - https://docs.blender.org/manual/en/latest/files/media/image_formats.html
  - https://docs.blender.org/api/current/bpy.types.ImageFormatSettings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# png-jpeg-tiff-settings

Goal: the right image file for each use: review, delivery, texture or comp.

## Output Properties > Output

- **Media Type**: Image, Multi-Layer EXR, or Video. With Image, **File Format** offers JPEG, OpenEXR, PNG, WebP, AVIF, BMP, Cineon, DPX, Iris, JPEG 2000, Radiance HDR, Targa, Targa Raw and TIFF.
- **Color**: BW, RGB, RGBA. RGBA is not available for every format (JPEG has no alpha); a transparent background also needs Render Properties > Film > **Transparent**.
- **Color Depth**: formats differ. PNG and TIFF 8 or 16 bit, JPEG 8 bit, DPX and Cineon 8, 10, 12 or 16 bit, JPEG 2000 8, 12 or 16 bit, OpenEXR Float (Half) or Float (Full).
- **Compression** (PNG and similar): 0 to 100, default 15 per the Python API. For PNG it only trades file size against write time (lossless).
- **Quality** (lossy formats such as JPEG): 0 to 100, default 90 per the Python API; lower means more loss.
- TIFF **Compression** (`tiff_codec`): None, Deflate (default), LZW, Pack Bits.
- **Color Management** (panel in Output): Follow Scene, or Override with its own view and display for this output.
- **Save As Render** (in Image Editor Save As): saves with the render's colour management; for PNG that applies the view and display transform, for EXR the default render output space.

## Choosing

The manual's rule of thumb: OpenEXR for compositing or grading, PNG for on-screen output or encoding to several video formats, JPEG where size matters and quality loss is acceptable.

| Use | Format |
|---|---|
| Web or still delivery | PNG 8-bit RGB(A), or JPEG |
| Heavy grading of a still | PNG or TIFF 16-bit |
| Comp, multipass | OpenEXR, or Multi-Layer EXR |
| Film/DI legacy | DPX |
| Baked data maps (normal, height) | PNG 16-bit or EXR, colour space Non-Color (practice) |

## Gotchas

- Banding in smooth gradients: use a higher bit depth, or the Post Processing > **Dither** setting (documented as reducing visible banding).
- The Override colour management option is easy to forget. A shot that "looks different" on disk may have it set.

## Verify

Open the file in an external viewer and check bit depth and alpha.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): output.rst (Media Type, Color, Color Management Follow Scene/Override), image_formats.rst (format list, channel depth and alpha table, Save As Render, rule of thumb), film.rst (Transparent), post_processing.rst (Dither), and the current Python API ImageFormatSettings (compression 0-100 default 15, quality 0-100 default 90, tiff_codec values and default). Removed: unverified alpha-premultiplication claim, the oiiotool/magick check command, the "15 percent is fine" advice, "90 is a good review value". Method: documentation only; no commands were run.
