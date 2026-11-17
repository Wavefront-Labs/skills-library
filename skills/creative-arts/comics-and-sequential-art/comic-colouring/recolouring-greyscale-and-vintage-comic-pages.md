---
id: creative-arts.comics-and-sequential-art.comic-colouring.recolouring-greyscale-and-vintage-comic-pages
name: recolouring-greyscale-and-vintage-comic-pages
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, digital-comic-colour, recolouring, restoration-colour]
level: advanced
status: draft
description: "Recolour or restore vintage and greyscale comic pages: cleaning scans, extracting line art from printed pages, re-flatting, and choosing faithful versus modern colouring."
sources:
  - https://books.google.com/books?vid=ISBN9780823010301
  - https://en.wikipedia.org/wiki/Ben-Day_process
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recolouring greyscale and vintage comic pages

**Goal:** a clean, reprint-ready page from old printed comics or greyscale art.

## Get clean line art
1. Source: original art or stats if available (best); otherwise the cleanest printed
   copy, scanned at 600-1200 ppi colour.
2. For printed colour pages: extract the black plate. Use channel separation
   (the K content dominates the darkest values); threshold carefully; descreen
   halftones (Photoshop descreen, blur then threshold) before converting to 1-bit.
3. Clean: remove paper texture, rebuild broken lines, fill crushed blacks, despeckle.
4. Greyscale art (wash or tones): keep the greyscale as a multiply layer and colour
   beneath, or convert to line plus tone.

## Recolour approaches
- Faithful restoration: match original palette, flat colour, optional Ben-Day dot
  texture; disclose restoration in the credits.
- Modern recolour: gradient rendering, lighting; can clash with simple line art;
  keep rendering restrained to suit the line.

## Rights
- Confirm the work is in the public domain or licensed; restored and recoloured
  editions can carry new copyright on the new contribution only.

## Verify
- [ ] Line art clean at 200 percent zoom with no halftone residue.
- [ ] Colour approach approved and noted in the edition credits.
