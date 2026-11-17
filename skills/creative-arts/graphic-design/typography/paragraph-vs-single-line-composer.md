---
id: creative-arts.graphic-design.typography.paragraph-vs-single-line-composer
name: paragraph-vs-single-line-composer
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, justification, text-alignment, paragraph-composer, single-line-composer, world-ready-composer, knuth-plass, line-breaking, text-wrap-pretty, indesign]
level: practitioner
status: draft
description: "Choose the line-breaking composer: Adobe Paragraph vs Single-line Composer (and World-Ready for complex scripts), how each affects spacing and edits, and web equivalents."
sources:
  - https://helpx.adobe.com/indesign/using/text-composition.html
  - https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Paragraph vs single-line composer

**Goal:** the most even spacing and best line breaks your software can give, with predictable behaviour when editing.

## The composers (InDesign / Illustrator / Photoshop Paragraph panel menu)
- **Adobe Paragraph Composer** (default): evaluates possible break points for the whole paragraph and picks
  the set that gives the most even spacing overall (inspired by the Knuth-Plass algorithm used in TeX).
  Result: better justified texture, fewer hyphens, nicer rags.
- **Adobe Single-line Composer:** breaks one line at a time, like a traditional typesetter working line by
  line. Spacing less even, but editing a line never changes earlier lines.
- **Adobe World-Ready Paragraph/Single-line Composers:** required for Arabic, Hebrew, Indic and other complex
  scripts (right-to-left, shaping). Set it on styles used for those languages; Latin text sets fine with it too.

## When to use which
| Situation | Composer |
|---|---|
| Body text, justified or ragged | Paragraph |
| Late-stage corrections where reflow of previous lines must not happen (approved magazine pages, legal text) | Single-line on that paragraph, carefully |
| Hand-tuned display text where you control every break | Single-line (predictable) or Paragraph + forced breaks |
| Complex scripts | World-Ready |

## Side effects to know
- With the paragraph composer, editing a word near the end can change line breaks **earlier** in the paragraph.
  Proofreaders' "only one word changed" can move three lines - reproof the whole paragraph.
- It may choose a slightly looser line early to avoid a terrible line later - which is the point.

## Web
Browsers break greedily (single-line style). CSS **`text-wrap: pretty`** asks the browser to optimise the last
lines/whole paragraph (paragraph-composer-like, supported in recent Chromium and Safari); **`text-wrap: balance`**
evens lines in headings. Progressive enhancement: older browsers ignore them.

## Verify
- [ ] Body styles use Paragraph Composer (or World-Ready for complex scripts).
- [ ] After late edits, the whole paragraph was re-proofed.
