---
id: creative-arts.graphic-design.adobe-photoshop.image-processor-and-scripts
name: image-processor-and-scripts
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-automation, image-processor, scripts, export-layers-to-files, load-files-into-stack]
level: practitioner
status: draft
description: "Use Photoshop's built-in scripts: Image Processor for multi-format resizing, Export Layers to Files, Load Files into Stack, and running custom JSX/UXP scripts."
sources:
  - https://helpx.adobe.com/photoshop/using/processing-batch-files.html
  - https://helpx.adobe.com/photoshop/using/scripting.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Image Processor and scripts

## Image Processor (File > Scripts > Image Processor)
Quickest way to output JPEG + PSD + TIFF versions of a folder at a max size.
1. Select images: open images or a folder (include subfolders); optionally open first image to apply settings.
2. Location: same folder (creates JPEG/PSD/TIFF subfolders) or a chosen folder.
3. File types: Save as JPEG (quality 0-12, **Convert Profile to sRGB**), PSD (Maximize
   compatibility), TIFF (LZW). Each with **Resize to Fit** W x H px - fits within the box, keeps proportions.
4. Preferences: Run Action (e.g. sharpening set) on each, Copyright info, Include ICC Profile.

## Other built-in scripts
- **Export Layers to Files** - each layer to its own file (prefix, format, trim layers).
- **Load Files into Stack** - many images as layers in one doc; Attempt to Automatically Align
  for focus stacks or exposure blends.
- **Statistics** - stack mode median to remove moving people from multi-shot tourist photos.
- **Layer Comps to Files** - per comp output.

## Custom scripts
- File > Scripts > Browse to run a `.jsx` (ExtendScript) script; place scripts in the
  Presets/Scripts folder to list them in the menu (restart required).
- Newer UXP scripts (`.psjs`) run from File > Scripts > Browse in current versions.
- Scripts can be recorded into actions (Insert Menu Item > File > Scripts > ...).

## Gotchas
- Image Processor resizes with the default interpolation in Preferences; set Bicubic Sharper/Automatic first.
- Large batches: close other documents; the script opens each file.

## Verify
- [ ] Output folders contain expected formats and sizes; profile is sRGB for web JPEGs.
