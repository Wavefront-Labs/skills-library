---
id: creative-arts.graphic-design.adobe-indesign.page-numbering-and-sections
name: page-numbering-and-sections
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-document-setup, numbering-and-section, facing-pages, spreads, roman-numerals, section-prefix, pages-panel, allow-pages-to-shuffle, gatefold]
level: practitioner
status: draft
description: "Control InDesign pagination: facing pages, Numbering and Section Options (roman front matter, restarts, prefixes), left-page starts and gatefold spreads."
sources:
  - https://helpx.adobe.com/indesign/using/numbering-pages-chapters-sections.html
  - https://helpx.adobe.com/indesign/using/pages-spreads.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Page numbering, sections and spreads

**Goal:** folios that match the publication's pagination (roman front matter, arabic body, section
prefixes) and spreads that reflect how the printed piece opens.

## Sections (Pages panel > right-click a page > Numbering & Section Options)
- **Start Section** at this page; **Start Page Numbering at** a number, or Automatic.
- **Style:** 1, 2, 3 / i, ii, iii / I, II / a, b - e.g. front matter i-xii, then a new section at the
  first chapter starting at 1.
- **Section Prefix** (e.g. `A-`) and "Include Prefix when Numbering Pages" - useful in manuals (A-1, B-1).
- **Section Marker** text, inserted with Type > Insert Special Character > Markers > Section Marker -
  shows the section name in running heads.
- A small black triangle above the page icon in the Pages panel marks a section start.
- Pages panel numbering display: Preferences > General > Page Numbering View: Absolute (1, 2, 3 in order)
  vs Section numbering - use Absolute when printing ranges if confused; PDF export page ranges use the
  same choice (`+5` means absolute page 5).

## Facing pages and spreads
- Page 1 is a right-hand (recto) page; even numbers are left (verso). That is a printing convention - keep it.
- Starting on a left page: Document Setup Start Page # = 2, or section start at an even number.
- **Gatefolds and multi-page spreads:** Pages panel menu > untick **Allow Document Pages to Shuffle**
  (or Allow Selected Spread to Shuffle), then drag a page next to a spread to make a 3- or 4-page spread.
  Fold-in panels are often narrower (2-3 mm) than the cover pages - use the Page tool (Shift+P) to resize
  individual pages.
- Cover spreads with spine: one spread of back cover + spine + front cover with different page widths
  (Page tool), or a single-page document for the cover.

## Folios
Put the **Current Page Number** marker (Alt+Shift+Ctrl+N / Opt+Shift+Cmd+N) in a text frame on the parent
pages (see auto page numbers skill). Pages with full-bleed images can use a "None" parent or a parent
without folio.

## Gotchas
- Inserting an odd number of pages in a facing-pages document swaps left/right for every later page -
  check images that bleed into the gutter.
- Blank pages still count in pagination; printers need the total multiple of 4 (saddle stitch) or 8/16 (signatures).

## Verify
- [ ] Pages panel sections and styles match the pagination plan; TOC numbers agree.
- [ ] Recto/verso correct for chapter openers; page total suits the binding.
