---
id: creative-arts.graphic-design.adobe-illustrator.new-document-profiles-and-raster-effects
name: new-document-profiles-and-raster-effects
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, ai-document-setup, document-raster-effects-resolution, document-profiles, color-mode, units]
level: intro
status: draft
description: "Set up Illustrator documents correctly: print/web/mobile profiles, colour mode, units, bleed, and Document Raster Effects Resolution for print-quality effects."
sources:
  - https://helpx.adobe.com/illustrator/using/create-documents.html
  - https://helpx.adobe.com/illustrator/using/about-effects.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# New document profiles and raster effects resolution

## New Document dialog (Ctrl/Cmd+N)
- **Print**: CMYK, points/mm, Document Raster Effects 300 ppi, bleed 3 mm (or 0.125 in).
- **Web / Mobile**: RGB, pixels, 72 ppi raster effects, Align New Objects to Pixel Grid.
- **Film & Video**: RGB, pixels, video safe areas.
- Advanced Options: Color Mode, Raster Effects, Preview Mode.

## Document Raster Effects Resolution (Effect > Document Raster Effects Settings)
Drop shadows, glows, blurs, textures and some 3D effects are rasterised on output at this
resolution. A file made from a Web profile and sent to print will have **72 ppi soft shadows**.
- Set **300 ppi** for print before final output (and High for large-format at 150 ppi effective).
- Changing it alters the look of some effects (Gaussian blur radius in px is resolution dependent) - recheck.

## Colour mode
File > Document Color Mode (CMYK/RGB). One mode per document. Switching converts swatches
but out-of-gamut RGB colours change visibly when moved to CMYK.

## Units
Preferences > Units (General, Stroke, Type). Per-document override: File > Document Setup.
Type in pt, layout in mm is common for print.

## Gotchas
- Templates from the web profile carry 72 ppi effects; check before packaging.
- Bleed can be edited later in Document Setup; artboards need to stay inside the canvas limit (227 x 227 in standard, 2270 in for large canvas).

## Verify
- [ ] Document Raster Effects = 300 ppi for print; colour mode matches the output.
- [ ] Bleed set per the printer's spec.
