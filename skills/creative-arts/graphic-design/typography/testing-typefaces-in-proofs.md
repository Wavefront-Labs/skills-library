---
id: creative-arts.graphic-design.typography.testing-typefaces-in-proofs
name: testing-typefaces-in-proofs
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, typeface-selection, font-pairing, type-specimen-testing, type-proofing, waterfall, real-copy, print-proof, screen-rendering, legibility-testing]
level: practitioner
status: draft
description: "Evaluate shortlisted typefaces with real proofs: waterfalls, real copy at real sizes, print and screen renders, stress tests, and x-height-matched comparison."
sources:
  - https://www.papress.com/products
  - https://www.hartleyandmarks.com/products/the-elements-of-typographic-style
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing typefaces in proofs

**Goal:** choose a typeface from evidence - how it performs with this content, at these sizes, in this medium - not from a specimen's hero line.

## Build a test document
For each candidate (same layout, swap only the font):
1. **Waterfall:** the same paragraph at 7, 8, 9, 10, 11, 12, 14 pt (or 12-20 px) to see where it reads best.
2. **Real copy** at the intended size, leading and measure - a full column, not lorem ipsum. Include headings,
   captions, a table, footnotes.
3. **Stress tests:** numbers and prices (figures styles), all caps line, small caps, italics and bold in text,
   accents from all languages needed, punctuation-heavy text (quotes, dashes, parentheses), long words.
4. **Display line:** the headline at final size with the actual words (brand name, key headline).
5. Similar-letter test: `Il1| O0 rnm cl d` for UI/wayfinding/codes.

## Proof in the real medium
- **Print:** print on the target paper or close (laser on similar stock at minimum); uncoated paper makes light weights
  and thin serifs fragile.
- **Screen:** render in the actual environment (browsers on Windows and macOS, phone); text rendering differs; check
  hinting at small sizes, and reversed (light on dark) text.
- Look at arm's length and reading distance; read a few paragraphs fully - fatigue shows after a page.

## Compare fairly
- Match **x-heights**, not point sizes, when comparing (fonts at the same point size differ in apparent size).
- Same leading ratio and measure for each candidate.
- Get feedback from a few readers from the audience (older readers for health info, children for education).

## Decide
Score by criteria from the brief: legibility at size, tone, language coverage, family completeness, licence cost
(see font licensing). Document why the winner won.

## Verify
- [ ] Each candidate proofed with real copy in print and on screen, matched by x-height.
- [ ] Stress tests passed by the chosen face; decision rationale recorded.
