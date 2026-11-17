---
id: creative-arts.graphic-design.adobe-indesign.automatic-page-numbers
name: automatic-page-numbers
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, parent-pages, auto-page-numbers, folios, current-page-number, next-page-number, continued-on-jump-lines, section-marker]
level: intro
status: draft
description: "Add automatic folios in InDesign with the Current Page Number marker on parent pages, mirrored positions, dropped folios, and Next/Previous page jump lines."
sources:
  - https://helpx.adobe.com/indesign/using/numbering-pages-chapters-sections.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automatic page numbers (folios)

**Goal:** correct page numbers on every page, styled consistently, without typing a single number.

## Add folios
1. Open the parent page (double-click `A-Parent` in the Pages panel).
2. Draw a text frame where the folio goes on the **left** page; insert **Type > Insert Special Character >
   Markers > Current Page Number** (Alt+Shift+Ctrl+N / Opt+Shift+Cmd+N). It shows the parent prefix "A".
3. Duplicate the frame to the **right** page in the mirrored position (align outside edges).
4. Apply a `Folio` paragraph style (often tabular figures, small size, perhaps with the section name via Section Marker).
5. Document pages based on that parent now show the right numbers.

## Variations
- Folio + section name: `12 | Chapter title` using the marker plus a running head variable (see running heads skill).
- Numbering style (roman/arabic) and starts come from **Numbering & Section Options**, not the marker (see sections skill).
- Folios on pages with full-bleed images: apply a parent without folios (or `[None]`), or override and delete
  on that page; printers and readers accept "dropped folios" on image pages.

## Jump lines ("continued on page")
For stories continuing elsewhere (newspapers, magazines):
- Draw a small text frame **touching or overlapping** the story's frame, insert **Next Page Number** marker
  ("Continued on page X") - InDesign finds the page of the next threaded frame.
- At the continuation, **Previous Page Number** ("Continued from page X").
- Group the jump frame with the story frame so they move together.

## Gotchas
- Typing numbers by hand on document pages breaks when pages move. Always use the marker.
- A folio frame on the parent can be covered by images on document pages - put folios on a top layer
  (Layers panel) so they stay above.
- The marker shows the parent's letter on the parent page; that is normal.

## Verify
- [ ] Every page (except intentional dropped folios) shows the correct number.
- [ ] Left/right folios mirrored correctly; continued-on lines point to the right pages.
