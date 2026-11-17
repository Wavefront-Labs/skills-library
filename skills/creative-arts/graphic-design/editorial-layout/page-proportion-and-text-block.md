---
id: creative-arts.graphic-design.editorial-layout.page-proportion-and-text-block
name: page-proportion-and-text-block
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, book-design, page-proportion, text-block, type-area, van-de-graaf-canon, golden-section, margins, bringhurst, trim-size]
level: advanced
status: draft
description: "Choose book page proportions and the text block: classical ratios (2:3, golden section, 1:root 2), Van de Graaf and Tschichold canons, margin progression and practical trim sizes."
sources:
  - https://en.wikipedia.org/wiki/Canons_of_page_construction
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Page proportion and text block

**Goal:** a page shape and text block whose proportions feel settled, with margins that frame the text
and leave room for hands and binding (Bringhurst, The Elements of Typographic Style, ch. 8).

## Page proportions
| Ratio | Name | Typical use |
|---|---|---|
| 1:1.414 | ISO (root 2), A and B sizes | reports, European books |
| 1:1.5 (2:3) | | classic book, trade paperbacks (e.g. 6 x 9 in) |
| 1:1.618 | golden section | literary books, fine press |
| 1:1.25 (4:5) | | photo and art books |
| 1:1.333 (3:4) | | magazines, textbooks |
Practical trim sizes depend on the printer's sheet and press: ask before choosing, or waste and cost rise.

## Text block
- Give the text block the **same proportion as the page** (classical approach) or a deliberate contrast.
- **Van de Graaf canon / Tschichold's reconstruction:** on a 2:3 page, diagonals of the spread and the page
  locate a text block of the same proportion with margins in ratio **inner : top : outer : bottom =
  1 : 1.5 : 2 : 3** (Villard/Van de Graaf). The text block takes about half the page area, with inner margin
  1/9 of page width and top 1/9 of page height.
- Modern books with smaller margins usually keep the **progression**: inner smallest, then top, outer, bottom
  largest.

## Practical constraints
- Measure 45-75 characters (66 ideal) sets text block width before proportion arguments do.
- Perfect binding needs larger inner margins (add 3-6 mm for glue and curvature).
- Text block height must be a whole number of lines of leading (see modular-grid-fields-from-line-count).
- Thumb space: outer margins of at least 12-15 mm on paperbacks.

## Process
1. Pick trim size with the printer.
2. Set body type and measure.
3. Fit the text block height to whole lines; set margins in progression; check against a canon overlay.
4. Print a spread at 100% and judge by eye; adjust in whole lines and millimetres.

## Gotchas
- Classical canons give generous margins and high page counts; budget books cannot always afford them.
- Optical centre is above the geometric centre: equal top and bottom margins make the text look low.

## Verify
- [ ] Margins follow a progression (inner < top < outer < bottom, or justified exception).
- [ ] Text block height is a whole number of lines; measure is in range.
