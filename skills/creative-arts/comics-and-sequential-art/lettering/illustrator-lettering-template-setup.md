---
id: creative-arts.comics-and-sequential-art.lettering.illustrator-lettering-template-setup
name: illustrator-lettering-template-setup
category: creative-arts
field: comics-and-sequential-art
product: lettering
tags: [lettering, lettering-workflow, digital-lettering, illustrator-lettering, lettering-template, paragraph-styles, artboards, placed-art]
level: practitioner
status: draft
description: "Build a reusable Illustrator lettering template: artboard at trim with bleed and safe guides, locked art layer, text/balloon/SFX layers, paragraph and graphic styles, and page artboards."
sources:
  - https://helpx.adobe.com/illustrator/using/character-paragraph-styles.html
  - https://kleinletters.com/Blog/
  - https://www.comicbookfonts.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Illustrator lettering template setup

**Goal:** a template that makes every page consistent and fast to letter and export.

## Document
- Artboard = **trim size** (e.g. 6.625 x 10.25 in for a US comic); document bleed set
  (e.g. 0.125 in); colour mode per output (CMYK for print with K-only text, RGB for
  digital).
- Guides for the **safe/live area**; lock guides.
- One artboard per page, or one file per page; multi-artboard files speed batch export
  but get heavy.

## Layers (top to bottom)
```
NOTES (non-printing)
SFX
TEXT
BALLOONS
ART (placed, locked)
```
- Place art linked (File > Place, Link checked) so files stay light and update when
  art changes.
- Mark NOTES as non-printing (Layer Options > Print off).

## Styles
- **Paragraph styles**: Dialogue (font, size, leading, centred, tracking), Dialogue
  Small, Caption, Caption Narrator 2, Whisper.
- **Character style**: Emphasis (bold italic).
- **Graphic styles**: Balloon (white fill, black stroke at set weight), Caption box,
  Whisper balloon (dashed stroke), Electronic.
- Text colour 100K; balloon strokes 100K, fills white; set black text to overprint for
  print (see the overprint skill).

## Workflow helpers
- Actions for common tasks (unite balloon + tail, apply style).
- Save as template (.ait) so originals don't get overwritten.

## Verify
- [ ] Trim, bleed and safe guides correct for the publisher spec.
- [ ] Styles exist and are used (no local overrides).
- [ ] Art linked, not embedded; notes non-printing.
