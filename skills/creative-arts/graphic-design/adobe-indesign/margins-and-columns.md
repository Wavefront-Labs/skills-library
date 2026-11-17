---
id: creative-arts.graphic-design.adobe-indesign.margins-and-columns
name: margins-and-columns
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-document-setup, margins-and-columns, column-gutter, inside-outside-margins, layout-grid, create-guides, baseline-grid-setup]
level: practitioner
status: draft
description: "Set InDesign margins and columns for real layouts: inside margins for binding, columns and gutters per parent, Create Guides for rows, baseline grid fit."
sources:
  - https://helpx.adobe.com/indesign/using/ruler-guides.html
  - https://helpx.adobe.com/indesign/using/columns-margins.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Margins and columns

**Goal:** a type area and column structure that suits the content and binding, set up once on parent pages.

## Margins
- Facing pages use **Inside/Outside** instead of Left/Right. The inside margin must allow for binding:
  perfect-bound books lose 3-6 mm into the spine, so inside margins are often larger than they look
  necessary; saddle-stitched work loses little.
- Classical book proportions put more space at the bottom and outside than the top and inside (see page
  proportion skill); magazines often use near-equal margins with a slightly larger foot for folios.
- Keep body text at least 10-12 mm from the trim on small formats; folios and running heads may sit in the margin.
- Change later in **Layout > Margins and Columns** (affects the selected pages or parent).

## Columns
- Number and **gutter** (space between columns). Gutter usually equals or exceeds the body leading
  (e.g. 4-5 mm for 9/12 pt text); too narrow and the eye jumps columns.
- Different column counts per parent page: e.g. A-Parent 3 columns for features, B-Parent 5 columns
  for news pages. Set on the parent, apply to pages.
- Unequal columns: drag column guides with guides unlocked (View > Grids & Guides > Lock Column
  Guides off) - but then text frames do not auto-snap to symmetric columns; use with care.
- Text frames have their own column settings (Object > Text Frame Options), independent of page columns;
  **flexible width** columns adapt to frame width.

## Rows and modules
Layout > **Create Guides**: rows and columns with gutters, fit to Margins or Page - quick modular
grids for image placement (see modular grid skill for line-count-based fields).

## Match the baseline grid
Preferences > Grids: baseline grid **Start** relative to Top Margin, **Increment** = body leading.
Set the top margin so the first baseline sits on the grid; set the bottom margin so the type area height
is a whole number of leading increments (type area height = n x leading). Then columns end on a baseline.

## Gotchas
- Changing margins with **Adjust Layout** enabled moves and resizes objects - intended or not (see adjust layout skill).
- Margin and column settings are per page/parent, not per document; pages detached from parents keep old settings.

## Verify
- [ ] Inside margin allows for binding; type area proportional to page.
- [ ] Gutter >= leading; columns set on parent pages.
- [ ] Type area height is a multiple of the baseline increment.
