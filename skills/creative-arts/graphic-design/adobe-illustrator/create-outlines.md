---
id: creative-arts.graphic-design.adobe-illustrator.create-outlines
name: create-outlines
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-type, create-outlines, outline-text, font-embedding, missing-fonts, live-text, logo-files, package-fonts]
level: practitioner
status: draft
description: "Decide when to outline Illustrator type (logos, art for cutters and sign makers) and when not to (editable copy, accessible PDFs), keeping a live-text master."
sources:
  - https://helpx.adobe.com/illustrator/using/creating-type-outlines.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Create outlines (and when not to)

**Goal:** artwork that renders identically everywhere without missing fonts, while keeping editable text where it matters.

## How
Select type objects, **Type > Create Outlines** (Shift+Ctrl/Cmd+O). Each glyph becomes a compound
path, grouped per text object. To outline all text: Select > Object > All Text Objects, then Create Outlines.

## When to outline
- **Logos and wordmarks** in final delivery files (AI/EPS/SVG/PDF): recipients will not have the font
  and must not retype it.
- Artwork for **sign makers, vinyl cutters, laser/CNC, embroidery, screen printers** and others whose
  software does not handle fonts.
- Lettering you will **modify** glyph by glyph (custom ligatures, cutting into letters).
- Some printers ask for outlined text in supplied AI/EPS files (PDF/X with embedded fonts usually avoids this).

## When NOT to outline
- Documents with copy that may change (brochures, posters still in revision).
- PDFs for screen: outlined text is not searchable, selectable or accessible to screen readers.
- Small text in print: outlined text can render slightly heavier at small sizes on some RIPs than hinted
  font rendering; embedding fonts in PDF is cleaner.
- When the font licence allows embedding, a PDF with embedded fonts is preferable to outlines.

## Do it safely
1. Keep a **live-text master** file (`logo_master_LIVE.ai`), and produce outlined delivery copies
   (`logo_final_OUTLINED.ai`). Or duplicate the text layer, hide the live copy, outline the visible one.
2. Before outlining, fix kerning and tracking - after outlining you can only move shapes.
3. Check for missing-font substitutes first (Type > Resolve Missing Fonts / Find Font): outlining a
   substituted font bakes in the wrong typeface.

## Alternatives
- **File > Package** collects fonts (licence permitting) with the AI file for designers who will edit.
- Save PDF with fonts embedded (subset) for print.

## Verify
- [ ] Delivery copy: Type > Find Font shows no fonts in use (all outlined).
- [ ] Live-text master saved alongside.
- [ ] Outlines made from the correct font, not a substitute.
