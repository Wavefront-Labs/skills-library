---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.epub-and-kindle-export-from-csp
name: epub-and-kindle-export-from-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-export, csp-epub-export, fixed-layout-epub, kindle, reading-direction, clip-studio-paint-ex]
level: advanced
status: draft
description: "Export a comic as fixed-layout EPUB from Clip Studio Paint EX: reading direction, cover, spreads, metadata, then check with EPUBCheck and Kindle Previewer."
sources:
  - https://www.w3.org/publishing/epubcheck/
  - https://kdp.amazon.com/en_US/help
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EPUB and Kindle export

## Export (EX)
- **File > Export multiple pages > EPUB data** (EX only). Choose the page range, output size (long edge
  e.g. 1600-2560 px), format (JPEG/PNG) and quality.
- Reading direction comes from the story's binding settings: right binding = right-to-left (manga),
  left binding = left-to-right.
- Set title, author, publisher and cover (first page or a separate image) in the export settings or story
  information.
- Spread pages: set spread handling (export as two pages so readers display them together in landscape).

## Validate
- Run **EPUBCheck** on the output; fix errors before submitting to stores (Apple Books, Kobo, Google Play).
- Open in a fixed-layout capable reader (Apple Books, Thorium) to check order and spreads.

## Kindle
- Amazon accepts EPUB uploads for many books, but comics/manga go through **Kindle Create** or **Kindle
  Comic Creator** / **Kindle Previewer**, which convert fixed-layout EPUB to Kindle format with panel view
  options. Test in Kindle Previewer on phone, tablet and e-ink profiles.

## Image sizing
- Distributors commonly recommend long edge at least 1600-2048 px; keep file sizes reasonable (total EPUB
  well under store limits).
- Export in sRGB; greyscale manga as greyscale JPEG for smaller files.

## Gotchas
- Wrong binding direction reverses page order for manga.
- Missing metadata causes store rejection; fill title and author at minimum.
- PRO can't export EPUB from a story; it must be done in EX or a separate EPUB tool.

## Verify
- [ ] EPUBCheck passes; page order and spreads correct in a reader.
