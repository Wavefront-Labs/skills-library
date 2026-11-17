---
id: creative-arts.graphic-design.typography.paragraph-indication
name: paragraph-indication
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, justification, text-alignment, paragraph-indication, first-line-indent, space-between-paragraphs, pilcrow, outdent, baseline-grid-spacing, body-first]
level: intro
status: draft
description: "Choose how paragraphs are separated: first-line indents vs space between, no indent after headings, baseline grid spacing, and outdents or pilcrows."
sources:
  - https://www.papress.com/products
  - https://www.hartleyandmarks.com/products/the-elements-of-typographic-style
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paragraph indication

**Goal:** paragraphs that are clearly separate without breaking the texture of the text block.

## Two main conventions - use one, not both
1. **First-line indent:** classic for books and continuous reading. Indent = **1 em** (the type size) to roughly the
   leading; e.g. 10 pt text -> 10-12 pt indent. Bringhurst: at least one en, commonly one em.
   - **No indent on the first paragraph** after a heading, break or the start of a chapter (the position already
     signals a new paragraph): use a `Body First` style with indent 0.
2. **Space between paragraphs:** common in screen text, reports and manuals. Use **a full line space** (= leading)
   or a half line; on a baseline grid, the space must be a multiple of the grid (full line), or the next lines go off-grid.

Using both (indent + space) is redundant. Both absent (flush, no space) makes paragraphs disappear except by ragged last lines.

## Expressive alternatives (Lupton)
- **Outdent / hanging indent:** first line sticks out to the left - catalogues, bibliographies.
- **Pilcrow (¶) or ornament** run-in, with paragraphs continuous - historical/expressive texts.
- **Extreme indent** (to a column or half the measure) - a designed, modern look.
- Line break with space but indent in a narrow column - newspapers (indent only).

## Setting in tools
- InDesign: Paragraph style > Indents and Spacing: First Line Indent; Space Before/After. `Next Style` from
  `Body First` to `Body`. Use **Align to Grid: All Lines** with space after = leading increments.
- CSS: `p + p { text-indent: 1em; margin-top: 0; }` gives book-style indents only between consecutive paragraphs.

## Gotchas
- Justified text with indent and short last lines: the next paragraph's indent can align with a short previous
  line, hiding the break - rare, fix by editing.
- Lists, quotes and captions need their own spacing rules.

## Verify
- [ ] One convention used consistently; no indent after headings.
- [ ] Spacing respects the baseline grid where one is used.
