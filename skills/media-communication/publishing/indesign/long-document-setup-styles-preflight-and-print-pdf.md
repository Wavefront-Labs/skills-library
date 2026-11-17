---
id: media-communication.publishing.indesign.long-document-setup-styles-preflight-and-print-pdf
name: long-document-setup-styles-preflight-and-print-pdf
category: media-communication
field: publishing
product: indesign
tags: [indesign, adobe-indesign, page-layout, typesetting, desktop-publishing, dtp, parent-pages, master-pages, paragraph-styles, character-styles, object-styles, baseline-grid, book-file, indb, sections, page-numbering, running-heads, text-variables, table-of-contents, preflight, package, pdf-x-4, pdf-x-1a, bleed, export-epub, affinity-publisher, quarkxpress, scribus, publishing]
level: practitioner
status: draft
description: "Set up a long document in InDesign: document and parent pages, a style system, sections and running heads, Book files and TOC, then preflight, package and export a print-ready PDF/X."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Long-document setup, styles, preflight and print PDF in InDesign

**Goal:** a book-length InDesign layout that's driven by styles (so global changes take
seconds), paginates correctly, and exports a PDF the printer accepts first time.

## 1. Document setup (File › New › Document)
- **Page size = trim size**; Facing Pages on for books.
- **Margins** from the design spec; **bleed** typically 3 mm / 0.125 in on outside edges
  (confirm with printer); slug if you need production notes.
- **Primary Text Frame** on so text threads automatically through parent pages.
- Set a **baseline grid** (Preferences › Grids) matched to body leading if the design
  aligns text across columns/pages.

## 2. Parent pages (called master pages before InDesign 2022)
- Create parents for: chapter opener, standard text spread, blank, part title.
- Put **running heads** and **folios** on parents: folio = Type › Insert Special Character ›
  Markers › Current Page Number. Running heads via **Text Variables** (Type › Text
  Variables) set to "Running Header (Paragraph Style)" pulling the chapter title style.
- Apply parents by dragging onto pages or Pages panel › Apply Parent to Pages.
- Override a parent item on one page with Ctrl/Cmd+Shift+click — sparingly.

## 3. Style everything
- **Paragraph styles** for body, first paragraph (no indent), headings, block quotes,
  lists, captions, notes. Base them on a root "Body" style with **Based On** so changing
  the font once cascades.
- **Character styles** for italic, bold, small caps, superscript note references.
  Never apply local formatting; a "+" next to a style name means an override — clear it.
- **Next Style** chains heading → first paragraph → body for fast styling.
- **Object styles** for image frames and captions; **table/cell styles** for tables.
- Importing Word: File › Place with **Show Import Options** to map Word styles to
  InDesign styles; remove local formatting but preserve italics (via character styles).
- Use **GREP styles** for automatic rules (e.g. no break in "p. 12").

## 4. Long-document tools
- **Book file (.indb):** one InDesign file per chapter collected in a Book panel; set a
  **style source** document and Synchronize styles; continuous page numbering across files.
  Single-file layouts are fine for shorter books.
- **Sections** (Pages panel › Numbering & Section Options): roman numerals for prelims,
  arabic starting at 1 for the main text.
- **Table of contents:** Layout › Table of Contents from heading styles; update after
  every repagination.
- **Footnotes** are native; endnotes are supported in recent versions (*check yours*).
- Index: Window › Type & Tables › Index for embedded indexing (see indexing skills).
- Typography: Adobe Paragraph Composer, sensible hyphenation settings, keep options
  (keep heading with next lines) to avoid stranded heads.

## 5. Preflight and package
- **Live Preflight** (bottom-left of the window, or Window › Output › Preflight). Make a
  profile that flags: missing/modified links, overset text, missing fonts, RGB images
  (if printer wants CMYK), low effective resolution (e.g. under 300 ppi for print images),
  and transparency issues. Fix every red item.
- **File › Package** collects the INDD, fonts (check licence), links and an IDML for
  archive/hand-off.

## 6. Export print PDF
File › Export › Adobe PDF (Print):
- Preset per the printer's spec — commonly **PDF/X-4** (keeps live transparency) or
  **PDF/X-1a** (flattens; older workflows). Ask the printer.
- Marks and Bleeds: Use Document Bleed Settings; crop marks if requested (offset beyond bleed).
- Output: colour conversion and destination profile as the printer specifies.
- Export **cover** separately with the printer's spine width template.
- For ebooks: File › Export › EPUB (Reflowable) — then validate (see ebook-production skills).

## Gotchas
- Overset text in a hidden frame silently drops copy — preflight catches it.
- Text variables for running heads pull the *first* or *last* instance on the page; check
  pages with two headings.
- Spot colours left in a CMYK job get printed as an extra plate or mis-converted.

## Verify
- [ ] No local overrides ("+") on styles in body text.
- [ ] Folios and running heads correct on every page, absent on openers/blanks.
- [ ] TOC updated after final pagination.
- [ ] Preflight shows no errors; package created.
- [ ] Exported PDF opened in Acrobat: bleed present, fonts embedded, page count matches.
