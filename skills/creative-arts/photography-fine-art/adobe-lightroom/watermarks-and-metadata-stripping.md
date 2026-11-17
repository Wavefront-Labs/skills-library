---
id: creative-arts.photography-fine-art.adobe-lightroom.watermarks-and-metadata-stripping
name: watermarks-and-metadata-stripping
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, watermarking, lightroom-export, watermark-editor, metadata-stripping, gps-removal, lightroom-classic]
level: practitioner
status: draft
description: "Create text and graphic watermarks with the Lightroom Classic Watermark Editor and strip private metadata (GPS, people, camera data) on export."
sources: ["https://helpx.adobe.com/lightroom-classic/help/using-watermark-editor.html", "https://helpx.adobe.com/lightroom-classic/desktop/export-photos/exporting-photos-basic-workflow.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Watermarks and metadata stripping

## Watermark Editor (Edit > Edit Watermarks, any module)
- **Text**: font, style, alignment, colour, shadow (opacity, offset, radius, angle). Default text = your copyright line.
- **Graphic**: a PNG (with transparency) or JPEG logo. Use PNG white or black at 50-70% opacity.
- **Watermark Effects**: Opacity, Size (Proportional, Fit, Fill), Inset (horizontal/vertical), Anchor (9 positions), Rotate.
- Save as a preset (`Signature PNG 8%`).
- Simple Copyright Watermark (Export > Watermarking) uses the Copyright metadata field; nothing appears if the field is empty.

## Apply
- Export > Watermarking > tick and choose preset. Watermarks are available for JPEG, PSD, TIFF, PNG, AVIF and JPEG XL (not DNG/original).
- Also in Print module (Page panel > Watermarking) and Publish Services.

## Fine-art practice
- Many curators and reviewers dislike watermarks on submission images; most open calls forbid them. Use small, low-resolution files and metadata instead.
- For public web use, a small corner mark at 15-25% of width deters casual reuse; it does not prevent cropping or AI removal.

## Metadata stripping (Export > Metadata)
- Include: Copyright Only (strips camera, settings, keywords), or All Except Camera & Camera Raw Info.
- **Remove Person Info** (face-region names) and **Remove Location Info** (GPS) for home, sensitive species and private-location work.
- Keywords marked "Include on Export: off" are never written.

## Verify
- [ ] `exiftool -gps:all -RegionInfo exported.jpg` returns nothing; watermark position checks out on portrait and landscape exports.
