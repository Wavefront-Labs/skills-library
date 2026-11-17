---
id: creative-arts.graphic-design.typography.shaping-a-ragged-right
name: shaping-a-ragged-right
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, justification, text-alignment, rag, ragged-right, flush-left, hyphenation-zone, balance-ragged-lines, line-breaks, rag-shape]
level: practitioner
status: draft
description: "Set flush-left, ragged-right text with a good rag: no wedges, staircases or deep holes, controlled hyphenation, and hand-adjusted line breaks in display text."
sources:
  - https://helpx.adobe.com/indesign/using/text-composition.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shaping a ragged right

**Goal:** a right edge that looks organic and calm - line lengths varying gently, without patterns that catch the eye.

## What a good rag looks like
- Lines alternate gently long and short; the variation is a small fraction of the measure.
- No **wedges** or **staircases** (lines getting progressively shorter/longer in a diagonal).
- No very short line followed by a long one creating a hole; no line much shorter than all others mid-paragraph.
- Last lines of paragraphs may be short - but not a single short word (see widows/orphans skill).
Lupton: a ragged edge should be "soft and unforced"; Bringhurst prefers modest hyphenation over a jagged rag.

## Settings (InDesign)
- Align Left, Adobe Paragraph Composer.
- **Hyphenation** on for body text with conservative limits (words of 6+ letters, 3/3, max 2 consecutive);
  **Hyphenation Zone** (e.g. 10-15 mm): bigger zone = fewer hyphens, looser rag.
- Word spacing in Justification still applies (keep desired at 100%; min/max 80/120% in ragged text is fine).
- **Balance Ragged Lines** (Paragraph panel menu) for headlines and short centred/ragged text: evens line lengths
  (makes the first line shorter than the second if needed). Not for body text.

## By hand (display text, headlines, short copy)
- Break lines by sense: keep phrases together ("the / new building" bad, "the new / building" better); avoid ending
  lines with articles, prepositions or "a/I".
- Use **forced line breaks** (Shift+Enter) or **No Break** on word pairs; never hard returns inside a paragraph.
- Edit copy (with the writer's consent) when a line cannot be fixed - common in advertising.
- Body text: adjust only the worst spots, after copy is final; tiny tracking (+/-5) on a paragraph can help.

## Gotchas
- Very narrow measures (<35 characters) make good rags hard - widen the column or accept hyphenation.
- Different screen/browser rendering means web rags cannot be hand-tuned; use CSS `hyphens: auto` with the correct
  `lang`, and `text-wrap: pretty` (supported in modern Chromium/Safari) to improve rags automatically.

## Verify
- [ ] Squint at the column: no visible wedges, holes or staircases.
- [ ] Hyphens no more than 2 in a row; no single-word final lines in key paragraphs.
