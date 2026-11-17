---
id: creative-arts.visual-art.procreate.adding-and-editing-text
name: adding-and-editing-text
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, procreate-text, text-layer, fonts, kerning, import-font, rasterize-text, lettering]
level: practitioner
status: draft
description: "Add and edit text in Procreate: the Add text tool, style panel (font, kerning, tracking, leading), importing fonts, and rasterising text layers."
sources: ["https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Text in Procreate

**Goal:** typeset words on a canvas for posters, signs and comics.

## Steps
1. **Actions (wrench) > Add > Add text**. A text box and the keyboard appear; type, then tap outside the keyboard area.
2. Select the text and tap **Edit style** to open the panel: font, size, style (bold, italic), **Design** (kerning, tracking, leading and baseline), and **Attributes** (colour, opacity, underline and others as listed in the Handbook).
3. Move, scale and rotate the box with the transform handles. Text lives on a **text layer** that remains editable.
4. To use a font not on the list, install it on the iPad (through Files or a font app) and re-open the font picker; Procreate lists installed fonts. Only use fonts whose licence allows your use.
5. To paint on, apply effects or warp it, tap the layer and **Rasterize**. After rasterising, text is pixels and cannot be edited as text.

## Tips
- Keep a duplicated unrasterised text layer hidden as a backup.
- Use leading and tracking to fit lettering to a shape, then Warp (Transform) for curves; see `creative-arts.visual-art.procreate.transform-warp-and-liquify`.
- Variable fonts and OpenType alternates may or may not be exposed; unconfirmed per font.

## Gotchas
- A missing font on another device does not matter after rasterising, but it does for editable files shared as .procreate.
- Large type on small canvases looks blurry when exported; set canvas DPI for the output (`creative-arts.visual-art.procreate.canvas-setup-and-export-for-print-and-web`).

## Verify
- [ ] Text remains editable until you choose Rasterize.
- [ ] Font, spacing and colour changes appear in the live preview.
