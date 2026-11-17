---
id: creative-arts.graphic-design.adobe-indesign.document-setup-bleed-and-slug
name: document-setup-bleed-and-slug
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-document-setup, bleed-and-slug, bleed, slug, trim-size, document-presets, intent-print, facing-pages, primary-text-frame]
level: practitioner
status: draft
description: "Set up an InDesign print document right first time: trim size, intent, facing pages, bleed and slug values, primary text frame and saved presets, matched to the printer's spec."
sources:
  - https://helpx.adobe.com/indesign/using/create-documents.html
  - https://helpx.adobe.com/indesign/using/document-presets.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Document setup: bleed and slug

**Goal:** a document whose page size, bleed and slug match the printer's specification
before a single object is placed.

## New Document (Ctrl/Cmd+N)
1. **Intent:** Print (units default to points/mm, swatches CMYK). Web/Mobile switch units to
   pixels and swatches to RGB.
2. **Width/Height = trim size** (the finished, cut size), never trim + bleed.
3. **Facing Pages:** on for anything bound (books, magazines, brochures); off for single
   sheets, posters, flyers, business cards.
4. **Number of Pages** and **Start #** (start on 2 if page 1 is a left-hand page - rare).
5. **Primary Text Frame:** on for text-heavy books (text auto-flows across the parent's
   frame); off for designed brochures.
6. Columns and margins: see the margins and columns skill.
7. Expand **Bleed and Slug**:
   - **Bleed** typically **3 mm** (Europe/most digital) or **0.125 in** (US). Some printers
     want 5 mm for perfect-bound covers or large format. Facing pages: set Inside bleed to 0
     on bound jobs where the spine is not trimmed.
   - **Slug** (area outside bleed for job info, approval notes, colour bars) e.g. 10 mm at the
     bottom. It prints only when "Include Slug Area" is ticked at export.
8. Save Preset (icon next to the name) for repeat formats: `A5-portrait-3mm-bleed`.

## After creation
- File > Document Setup changes size/bleed later; Adjust Layout (see that skill) can
  move/resize objects to the new size.
- View > Screen Mode > Bleed shows the bleed area; Preview hides everything outside trim.
- Put job info in the slug with text variables (File Name, Output Date).

## Common printer specs to ask for
Trim size, bleed amount, safe/quiet zone (keep text 3-5 mm inside trim), binding (saddle
stitch needs creep allowance, perfect binding a spine width), colour profile and PDF preset.

## Gotchas
- Building the page at trim + bleed (e.g. 216 x 303 mm for A4) instead of A4 + 3 mm bleed
  makes crop marks wrong and the printer will reject or re-crop it.
- Bleed values entered after layout do not extend existing images - pull edge images out to
  the bleed guide.

## Verify
- [ ] Document Setup shows trim size equal to the finished size.
- [ ] Bleed guide (red) visible; every edge-touching object reaches it.
- [ ] Settings saved as a preset if the format recurs.
