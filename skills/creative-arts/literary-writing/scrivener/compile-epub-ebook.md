---
id: creative-arts.literary-writing.scrivener.compile-epub-ebook
name: compile-epub-ebook
category: creative-arts
field: literary-writing
product: scrivener
tags: [literary-writing, scrivener, scrivener-3, compile, scrivener-compile, compile-epub, epub3, ebook, kindle, cover-image, metadata, table-of-contents, epubcheck]
level: practitioner
status: draft
description: "Compile an EPUB 3 ebook from Scrivener 3: ebook format and section layouts, metadata and cover, front and back matter, table of contents."
sources: ["https://www.literatureandlatte.com/learn-and-support/user-guides", "https://www.w3.org/publishing/epubcheck/", "https://kdp.amazon.com/en_US/help"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compiling an ebook (EPUB) from Scrivener

**Goal:** a clean EPUB 3 from the same binder you use for the manuscript, ready for
KDP and wide retailers. Scrivener 3; menu and pane names differ slightly between
macOS and Windows.

## Prepare the project
- Section types assigned (Chapter, Scene, Front Matter...) — see
  `creative-arts.literary-writing.scrivener.compile-to-manuscript-format`.
- Ebook front matter documents (title page, copyright page) in a Front Matter folder;
  back matter (acknowledgements, about the author, also by, newsletter link) in a Back
  Matter folder. Keep front matter short so retailer samples reach the story.
- Cover image (JPEG) imported into the binder (e.g., in Research).

## Compile
1. **File > Compile**; at the top choose **Compile for: ePub 3 eBook** (Scrivener 3's
   EPUB output). (Amazon now takes EPUB for Kindle; older MOBI/KindleGen workflows are obsolete.)
2. Choose an ebook **format** (e.g., the built-in "E-book" format) or duplicate and edit one.
3. **Assign Section Layouts:** chapter headings, scene text, front-matter pages
   (ebook layouts usually have no page-break assumptions or headers/footers).
4. **Right-hand pane:**
   - Contents: tick what's included; add front/back matter folders.
   - **Metadata:** title, author(s), language, publisher, date, unique identifier
     (ISBN if you have one for the ebook), description.
   - **Cover:** choose the cover image from the binder.
   - **Table of contents:** generated from chapter titles — check it includes what you
     want (chapters, not scenes).
5. Format options in the format editor: scene separator (a centred ornament), first-line
   indents, no indent after headings; avoid hard-coded fonts and sizes.
6. Compile to a .epub file.

## Validate and preview
- Run **EPUBCheck** and fix errors (often from odd characters, broken links, or images).
- Preview in Kindle Previewer, Apple Books and an e-reader; check TOC links, scene
  breaks, italics, dark mode. See
  `creative-arts.literary-writing.novel-writing.ebook-formatting-epub` for checks.

## Gotchas
- Manuscript formatting (double spacing, Courier, headers) leaking into the ebook — use
  an ebook format, not the manuscript one.
- Scene breaks rendered as blank lines (lost at screen breaks) — set a visible separator.
- Every scene appearing in the TOC — limit the TOC to chapter level.

## Verify
- [ ] Compiled with an ebook format and correct metadata and cover.
- [ ] EPUBCheck passes.
- [ ] TOC lists chapters; scene separators visible on devices.
