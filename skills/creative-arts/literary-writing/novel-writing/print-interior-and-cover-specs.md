---
id: creative-arts.literary-writing.novel-writing.print-interior-and-cover-specs
name: print-interior-and-cover-specs
category: creative-arts
field: literary-writing
product: novel-writing
tags: [literary-writing, novel-writing, self-publishing, indie-publishing, print-interior, cover-specs, trim-size, bleed, gutter, spine-width, full-wrap-cover, book-design, typesetting, kdp-paperback]
level: practitioner
status: draft
description: "Build a print-ready novel interior and full-wrap cover: trim size, gutter margins by page count, bleed, spine width from page count and paper, fonts and running heads."
sources: ["https://kdp.amazon.com/en_US/help", "https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Print interior and cover specs

**Goal:** an interior PDF and a full-wrap cover PDF that pass KDP/IngramSpark checks and
look like a trade-published book. Always confirm numbers in the platform's current guide.

## Interior
- **Trim size:** common fiction sizes 5 x 8 in, 5.25 x 8 in, 5.5 x 8.5 in, 6 x 9 in.
  Smaller trims raise page count (and print cost); check comparable books.
- **Margins:** the inside (gutter) margin must grow with page count because thick books
  curve into the spine. KDP's minimum table, without bleed outside margins at least 0.25 in:
  | Pages | Min inside margin |
  |---|---|
  | 24-150 | 0.375 in |
  | 151-300 | 0.5 in |
  | 301-500 | 0.625 in |
  | 501-700 | 0.75 in |
  | 701-828 | 0.875 in |
  Real books use more than the minimums (around 0.75 in outside/top/bottom is typical).
- **Bleed:** only needed if images run off the page: add 0.125 in to the top, bottom and outside.
- **Typography:** a book serif (e.g. Garamond, Minion, Caslon) at about 10.5-12 pt with
  about 120-140% leading; justified text with hyphenation on; first paragraph of a chapter
  and after scene breaks not indented.
- **Running heads and folios:** author name verso, title recto (or chapter title);
  no headers or page numbers on chapter-opening pages and blank pages.
- **Chapters** start on a new page (recto starts are traditional but add pages).
- Avoid widows and orphans; check for rivers in justified text.
- Export PDF with all fonts embedded (PDF/X-1a for IngramSpark).

## Cover (full wrap: back + spine + front)
- Width = bleed + back + spine + front + bleed; height = bleed + trim height + bleed.
- **Spine width** = page count x paper thickness. KDP figures: white paper about
  0.002252 in/page, cream about 0.0025 in/page. Use the platform's cover calculator or
  template rather than doing it by hand.
- KDP: spine text only if the book has enough pages (79+ at time of writing); keep spine
  text clear of the folds by about 0.0625 in.
- Leave the barcode area clear on the back (KDP places it if you don't).
- 300 ppi images; keep text 0.125 in+ inside trim (safe zone).

## Proof
Order a printed proof: check gutter readability, spine centring, colour, font size.

## Verify
- [ ] Interior margins meet the page-count table; fonts embedded.
- [ ] Cover dimensions taken from the platform template for the final page count.
- [ ] Platform previewer reports no errors.
- [ ] Printed proof approved.
