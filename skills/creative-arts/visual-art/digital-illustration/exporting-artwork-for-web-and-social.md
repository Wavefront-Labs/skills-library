---
id: creative-arts.visual-art.digital-illustration.exporting-artwork-for-web-and-social
name: exporting-artwork-for-web-and-social
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, colour-management, web-export, social-media, srgb, jpeg-quality, png, webp, resizing, sharpening, aspect-ratio, metadata]
level: intro
status: draft
description: "Export art for web and social: convert to sRGB and embed it, size to the platform's long edge, JPEG/PNG/WebP choices, output sharpening, crops for 4:5 and 9:16, and metadata."
sources: ["https://docs.krita.org/en/general_concepts/file_formats.html", "https://helpx.adobe.com/photoshop/using/export-artboards-layers.html", "https://developers.google.com/speed/webp"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exporting artwork for web and social

**Goal:** online images that look like the original: correct colour, sharp, a
sensible file size (Krita file format docs; Photoshop Export As; WebP docs).

## Colour
- **Convert to sRGB** (not assign) before exporting if the document is in a wider
  space; **embed** the profile. Many apps and platforms assume sRGB and strip or
  ignore other profiles.

## Size
- Export a copy; never downsample the master.
- Size to the long edge the platform displays (commonly 1080-2048 px for social
  posts; check current platform guidance, it changes). Uploading far larger lets the
  platform resample, often softly.
- Crops: social feeds favour **4:5** portrait and **1:1**; stories/reels **9:16**.
  Plan safe areas so key content survives automatic crops.

## Format
| Format | Use |
|--------|-----|
| JPEG (quality ~80-92) | Paintings, gradients, photos; small files |
| PNG | Flat colour, line art, transparency; larger files |
| WebP | Smaller than JPEG at similar quality; good for your own website |

## Sharpening
Downscaling softens; apply light **output sharpening** after resizing (e.g. unsharp
mask small radius 0.3-0.6 px), judged at 100 percent zoom.

## Metadata and protection
- Add artist name and copyright in metadata (some platforms strip it).
- Watermarks reduce casual reuse but distract; keep subtle if used.
- Note AI-training opt-out tags/platform settings where offered.

## Gotchas
- Exporting a P3/Adobe RGB file without conversion: dull or oversaturated online.
- PNG for detailed paintings: huge files.
- Text or signature in the area that a 4:5 or 9:16 crop removes.

## Verify
- [ ] sRGB embedded; colours match the master on a calibrated screen.
- [ ] Platform-appropriate size and crop.
- [ ] Sharp at 100 percent without halos.
