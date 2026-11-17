---
id: creative-arts.comics-and-sequential-art.comic-colouring.overprinting-black-line-art-and-trapping
name: overprinting-black-line-art-and-trapping
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, print-colour, cmyk-comics, overprint-black, trapping, misregistration, knockout, k-only-line-art]
level: advanced
status: draft
description: "Prevent white gaps on press: overprint 100K line art and lettering on colour instead of knocking out, run colour under lines, and when trapping matters for comic pages."
sources:
  - https://en.wikipedia.org/wiki/Overprinting
  - https://en.wikipedia.org/wiki/Trap_(printing)
  - https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Overprinting black line art and trapping

**Goal:** no white slivers or colour halos around lines and letters when plates
misregister slightly.

## The problem
Presses print C, M, Y and K on separate plates. Small registration shifts happen. If a
black line **knocks out** the colour beneath it (colour removed under the line), a shift
reveals white paper beside the line.

## The fix: overprint black
- Line art and lettering at **100K**, set to **overprint**: colour continues under the
  black, black prints on top. A shift then only moves colour under black (invisible).
- In raster workflows (Photoshop): colour flats fill under the lines (that's why flats
  run under/into lines), and the line layer is Multiply or a separate K channel. In
  layered PDFs from InDesign/Illustrator, set black text/lines to overprint (Illustrator:
  Attributes > Overprint Fill; InDesign's [Black] overprints by default per its
  preferences).
- Check with **Overprint Preview** (Acrobat Output Preview or InDesign/Illustrator
  View > Overprint Preview).

## Trapping (colour against colour)
Where two colours meet with no line between them, a slight overlap (trap, often
~0.1-0.25 pt in vector work) prevents gaps. Many printers apply trapping in their RIP;
ask before adding your own. Raster comic colour usually doesn't need manual traps
because lines cover most borders.

## Gotchas
- Rich black (4-colour) lines can't overprint cleanly; use 100K for lines.
- White text set to overprint disappears (white overprint = nothing). Ensure white
  elements knock out.
- Large solid black areas: printers may want rich black (see the rich black skill),
  but thin lines stay 100K.

## Verify
- [ ] Output Preview: lines and lettering on K plate only, overprinting.
- [ ] No white objects set to overprint.
- [ ] Printer's trapping policy confirmed.
