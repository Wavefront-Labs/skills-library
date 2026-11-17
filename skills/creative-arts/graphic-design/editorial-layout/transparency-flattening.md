---
id: creative-arts.graphic-design.editorial-layout.transparency-flattening
name: transparency-flattening
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, pdf-x, print-ready-pdf, transparency-flattening, flattener-preview, flattener-presets, stitching-lines, live-transparency, pdf-x-1a-flattening, spot-colour-transparency]
level: advanced
status: draft
description: "Handle transparency for print: when flattening happens (PDF/X-1a, EPS, old RIPs), flattener presets and preview, stitching lines, spot-colour pitfalls, and live transparency."
sources:
  - https://helpx.adobe.com/indesign/using/flattening-transparent-artwork.html
  - https://www.gwg.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transparency flattening

**Goal:** transparent effects (drop shadows, opacity, blend modes, feathers) that print exactly as designed.

## Live vs flattened
- **PDF/X-4** (PDF 1.6) keeps transparency **live**; modern RIPs (Adobe PDF Print Engine) render it natively. This is the
  safest route - use it unless the printer cannot.
- **PDF/X-1a**, **PDF/X-3**, EPS and printing to older PostScript RIPs **flatten**: overlapping transparent areas are
  split into opaque pieces, some vector, some rasterised.

## Flattening problems
- **Stitching lines:** thin white lines where rasterised and vector pieces meet - often only on screen (anti-aliasing in
  Acrobat - turn off Smooth line art to check), sometimes in print.
- **Text near transparency** rasterised or converted to outlines (looks heavier), especially text under a drop shadow.
- **Spot colours with blend modes** can produce unexpected process builds or knockouts.
- Low raster resolution on gradients/feathers if the preset is low.

## Control it
- **Flattener presets** (Edit > Transparency Flattener Presets): **[High Resolution]** for print (Raster/Vector Balance
  100, Line Art and Text 1200 ppi, Gradient and Mesh 300 ppi); tick Convert All Text to Outlines only if needed;
  Clip Complex Regions reduces stitching.
- **Flattener Preview** panel (Window > Output) highlights areas that will be flattened (rasterised complex regions,
  outlined text, transparent objects).
- Design habits for flattened workflows: put text on a layer **above** all transparency; avoid transparency over spot
  colours; set the Transparency Blend Space to CMYK (Edit > Transparency Blend Space) in print documents.

## Gotchas
- Flattening happens at export/print, not in your file - you only see results in the PDF. Always check the flattened PDF
  with Output Preview at high zoom.
- Mixing RGB and CMYK transparency can shift colours when flattened in a different blend space.

## Verify
- [ ] PDF/X-4 used where the printer accepts it.
- [ ] If flattening: Flattener Preview reviewed, [High Resolution] preset, text above transparency, PDF checked at 400%.
