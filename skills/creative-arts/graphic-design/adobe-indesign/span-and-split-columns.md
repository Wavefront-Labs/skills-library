---
id: creative-arts.graphic-design.adobe-indesign.span-and-split-columns
name: span-and-split-columns
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-text-frames, text-threading, span-columns, split-columns, paragraph-layout, multi-column-headings, balance-columns, flexible-width-columns]
level: practitioner
status: draft
description: "Let headings span several columns and split lists into sub-columns inside one InDesign text frame with Span Columns and Split Columns, plus balanced and flexible columns."
sources:
  - https://helpx.adobe.com/indesign/using/text-frames.html
  - https://helpx.adobe.com/indesign/using/formatting-paragraphs.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Span and split columns

**Goal:** headlines across a multi-column story and short lists in sub-columns, without separate text frames.

## Span Columns
1. Put the cursor in the heading paragraph. Paragraph panel menu > **Span Columns** (or Control panel icon).
2. **Paragraph Layout: Span Columns**, Span: All or a number (2, 3).
3. **Space Before Span / Space After Span** to set distance from body text.
Put it in the heading's paragraph style so every feature headline spans automatically. Text continues below
in the frame's columns.

## Split Columns
For lists (ingredients, glossary, contributors) inside a single-column frame:
- Paragraph Layout: **Split Column**, Sub-columns: 2-4, **Inside Gutter**, Outside Gutter, Space Before/After Split.
- Apply via a paragraph style (e.g. `List 2-col`).

## Related frame settings (Object > Text Frame Options)
- **Balance Columns:** evens the column lengths in a frame - useful for the last page of an article.
- **Column type:** Fixed Number, Fixed Width, or **Flexible Width** (columns added/removed as frame width
  changes, with a maximum width) - good with liquid layouts.
- Column rules (vertical lines between columns) in the Column Rules tab (CC 2019+).

## Gotchas
- Spanning paragraphs at the end of a frame can jump to the next frame unexpectedly - check keep options.
- Span Columns affects only that paragraph; consecutive spanned paragraphs need the setting each (style it).
- Baseline grid: spans can push body text off-grid; set space after span to a multiple of the leading.

## Verify
- [ ] Headline spans the intended columns via style; body text below stays on the baseline grid.
- [ ] Split lists readable with adequate inside gutter.
