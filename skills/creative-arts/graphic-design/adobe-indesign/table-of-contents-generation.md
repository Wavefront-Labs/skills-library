---
id: creative-arts.graphic-design.adobe-indesign.table-of-contents-generation
name: table-of-contents-generation
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, long-documents, table-of-contents, toc-styles, tab-leader, pdf-bookmarks, book-panel, update-toc]
level: practitioner
status: draft
description: "Generate and update an InDesign table of contents from paragraph styles: TOC styles, entry formatting, page-number tabs with leaders, PDF bookmarks, and multi-document books."
sources:
  - https://helpx.adobe.com/indesign/using/creating-table-contents.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Table of contents generation

**Goal:** a contents page built automatically from headings that updates in one click.

## Prerequisite
Headings must use **paragraph styles** (Chapter Title, H1, H2). A TOC can only collect
styled paragraphs. Fix local-formatted headings first.

## Build it (Layout > Table of Contents)
1. **Title:** "Contents" with its own style (or blank).
2. **Styles in Table of Contents:** add the heading styles in order (Chapter Title level 1,
   H1 level 2...).
3. For each included style set **Entry Style** (a paragraph style for the TOC line, e.g.
   `TOC 1`, `TOC 2`), **Page Number:** After Entry / Before / None, and **Between Entry and
   Number:** `^t` (tab).
4. Options: **Create PDF Bookmarks** (navigation in PDFs), **Replace Existing Table of
   Contents** when updating, **Include Book Documents** for multi-file books, Include Text on
   Hidden Layers off.
5. Click **Save Style** to save a TOC style (reuse for list of figures/tables with Caption styles).
6. OK and click to place the loaded TOC text.

## Format the entries
In the `TOC 1` paragraph style: **right-aligned tab** at the frame's right edge with a
**leader** (`. ` dot-space) - Tabs panel (Shift+Ctrl/Cmd+T), Align to Frame. Use a character
style for the page numbers (e.g. tabular figures). Indent `TOC 2` with left indent.

## Update
Layout > Update Table of Contents (place the cursor in the TOC first). Run it last, after
page flow is final, and again after any edit that moves pages.

## Gotchas
- Forced line breaks (Shift+Enter) in headings appear in the TOC as odd breaks; use
  `Remove Forced Line Break` option in TOC or a discretionary break.
- Page numbers in the TOC follow section numbering (roman for front matter, arabic after).
- Headings on hidden layers or pasteboard still get collected unless excluded.

## Verify
- [ ] Every chapter/heading appears with the right level and correct page number.
- [ ] Updating produces no manual edits lost (all formatting comes from styles).
- [ ] PDF bookmarks present in the exported PDF.
