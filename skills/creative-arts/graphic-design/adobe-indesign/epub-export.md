---
id: creative-arts.graphic-design.adobe-indesign.epub-export
name: epub-export
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, preflight, indesign-export, epub-export, reflowable-epub, fixed-layout-epub, export-tagging, articles-panel, epubcheck, ebook]
level: advanced
status: draft
description: "Export reflowable and fixed-layout EPUB from InDesign: style export tagging, Articles panel reading order, anchored images, alt text, metadata, cover and EPUBCheck validation."
sources:
  - https://helpx.adobe.com/indesign/using/export-content-epub-cc.html
  - https://www.w3.org/publishing/epubcheck/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EPUB export

**Goal:** an ebook that validates, reads in the right order and looks correct across reading systems.

## Reflowable vs fixed layout
- **Reflowable:** text reflows to the screen; reader controls fonts/size. Novels, non-fiction, text-led books.
  Layout fidelity is low - design with styles, not positions.
- **Fixed layout:** every page as designed (children's picture books, cookbooks, comics). Not accessible-friendly
  for text resizing; larger files.

## Prepare for reflowable
- Everything formatted by **paragraph and character styles**; local overrides do not survive well.
- **Export Tagging** in each style (Style Options > Export Tagging): map H1 -> `h1`, Body -> `p` with a class; set
  "Split Document" on chapter-title styles (creates separate XHTML per chapter).
- **Reading order:** stories export in page order or use the **Articles panel** (drag frames in reading order, tick
  "Use for Reading Order in Tagged PDF/EPUB").
- **Images:** anchor them in the text flow (inline/above line) so they appear at the right point; set
  **Object Export Options** > Alt Text and EPUB/HTML size (relative to page width, resolution 150 ppi+).
- Remove or anchor decorative objects; floating frames go to the end or wherever page order puts them.

## Export (File > Export > EPUB (Reflowable))
- Version EPUB 3.0. **Cover:** rasterise first page or choose an image (recommended: 1600x2400 px JPEG).
- Navigation: TOC style for the navigation TOC.
- Content: Format for images, CSS options (generate CSS, or add your own stylesheet), include embeddable fonts
  (only if licensed for ebook embedding).
- **Metadata:** title, author, publisher, ISBN identifier, language (File > File Info + export dialog).

## Validate
Run **EPUBCheck** (W3C) on the file; fix errors before submitting to stores. Test in Apple Books, Kobo, Thorium/
Adobe Digital Editions, and a Kindle previewer (Amazon converts EPUB to its formats).

## Gotchas
- Text on paths, overprint, complex wraps, and many effects do not export to reflowable EPUB.
- Forced line breaks and manual spacing produce odd results on small screens.
- Font embedding needs explicit ebook licence rights (see font licensing skill).

## Verify
- [ ] EPUBCheck passes with no errors.
- [ ] Reading order, images and navigation correct in at least two reading systems.
