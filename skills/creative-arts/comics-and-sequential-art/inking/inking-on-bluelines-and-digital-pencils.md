---
id: creative-arts.comics-and-sequential-art.inking.inking-on-bluelines-and-digital-pencils
name: inking-on-bluelines-and-digital-pencils
category: creative-arts
field: comics-and-sequential-art
product: inking
tags: [inking, inking-bluelines, digital-pencils-ink, inking-over-pencils]
level: practitioner
status: draft
description: "Ink over printed blue-line pencils or digital pencil files: printing bluelines at the right size and colour, layer setup for digital pencils, and delivering clean files."
sources:
  - https://books.google.com/books?vid=ISBN9780823010295
  - https://en.wikipedia.org/wiki/Blue_pencil_(editing)
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inking on bluelines and digital pencils

**Goal:** inking someone else's pencils without the original boards, cleanly
separable from the pencils.

## Bluelines (traditional inks over printed pencils)
1. Receive scanned pencils at 600 ppi, full board size.
2. Convert to greyscale, then colourise to light cyan (around C40 or RGB 120 200 255)
   at 30-50 percent opacity. Raise levels so lines are visible but light.
3. Print at 100 percent on bristol (11 x 17 inch for US comics) using an inkjet that
   handles heavy stock; check that the board feeds straight and margins are right.
4. Ink; then scan in colour or greyscale and drop the blue (channel mixer or
   select colour range), finish as 1-bit line art.

## Digital pencils
- Pencil layer on top of the document set to low opacity, blue colour (Layer
  colour in CSP; Colour overlay in Photoshop), locked.
- Ink on separate layers below or above; never ink on the pencil layer.
- Keep the file size, resolution (600 ppi line art) and bleed exactly as
  received.
- Deliver inks only (pencil layer deleted or hidden and flattened as required).

## Gotchas
- Printers scale "to fit" by default: turn off scaling or panels drift off template.
- Blue too dark survives the drop-out as grey noise.

## Verify
- [ ] Final file has no blue residue.
- [ ] Trim and bleed lines align with the original template.
