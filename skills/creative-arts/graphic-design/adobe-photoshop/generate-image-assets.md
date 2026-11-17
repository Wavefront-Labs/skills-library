---
id: creative-arts.graphic-design.adobe-photoshop.generate-image-assets
name: generate-image-assets
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-export, generate-image-assets, layer-name-export, asset-generation, retina-assets]
level: practitioner
status: draft
description: "Auto-export assets from layer names with Generate Image Assets: naming syntax for formats, quality, scale suffixes, folders and default settings."
sources:
  - https://helpx.adobe.com/photoshop/using/generate-assets-layers.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Generate Image Assets from layer names

**Goal:** a live pipeline where renaming a layer or group writes an image file automatically, updated on every save.

## Turn on
File > Generate > **Image Assets** (per document, ticked state saved). Photoshop creates a
folder `<docname>-assets` next to the saved PSD and writes files whenever the layer changes.

## Naming syntax (layer or group names)
- `button.png` - PNG-32 by default.
- `hero.jpg80` or `hero.jpg8` - JPEG quality 80% (number 1-10 or 1-100%).
- `icon.png8`, `icon.png24`, `logo.gif`, `logo.svg` (simple vector shapes only).
- Scaling: `200% hero@2x.jpg`, `50% thumb.png`, `300x200 card.jpg` (px, in, cm, mm units).
- Multiple outputs from one layer: comma-separate `hero.jpg80, 200% hero@2x.jpg80`.
- Subfolders: `icons/close.png`.

## Default settings
Create an empty layer named `default @1x, 200% @2x/` - every asset is written once at 1x and
once into an `@2x/` subfolder.

## Gotchas
- The document must be saved first; assets go next to the PSD.
- Hidden layers are still exported; delete or rename to stop output.
- Effects are included; content outside the canvas is trimmed to layer bounds, not canvas.
  For fixed-size exports, add a transparent mask/rectangle to set bounds.
- Export As (artboards/layers) is the newer manual alternative; Generator is best for repeating hand-off.

## Verify
- [ ] Assets folder contains every expected file at expected pixel sizes.
- [ ] Edit a layer, save, file timestamp updates.
