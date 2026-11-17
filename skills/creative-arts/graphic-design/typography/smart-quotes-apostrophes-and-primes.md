---
id: creative-arts.graphic-design.typography.smart-quotes-apostrophes-and-primes
name: smart-quotes-apostrophes-and-primes
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, typographic-details, punctuation, smart-quotes, apostrophe, primes, guillemets, typographers-quotes, language-specific-quotes, find-change]
level: intro
status: draft
description: "Use correct quotation marks and apostrophes (curly, not straight), primes for feet/inches and minutes, language-specific quotes and guillemets, and fix supplied copy automatically."
sources:
  - https://practicaltypography.com/straight-and-curly-quotes.html
  - https://helpx.adobe.com/indesign/using/glyphs-special-characters.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smart quotes, apostrophes and primes

**Goal:** no "dumb" straight quotes in typeset text, no backwards apostrophes, and real primes where measurements need them.

## The characters
| Name | Glyph | Unicode |
|---|---|---|
| Left/right double quote | “ ” | U+201C / U+201D |
| Left/right single quote | ‘ ’ | U+2018 / U+2019 |
| **Apostrophe** | ’ (same as right single quote) | U+2019 |
| Prime (feet, minutes) | ′ | U+2032 |
| Double prime (inches, seconds) | ″ | U+2033 |
| Guillemets | « » ‹ › | U+00AB/BB, U+2039/203A |
Straight `"` and `'` are typewriter characters - acceptable only in code.

## Common errors
- **Backwards apostrophe** at the start of abbreviated words: `'90s`, `'til`, `rock 'n' roll` - auto-quote
  turns them into opening quotes (‘). The apostrophe always points like a comma (U+2019). Fix by typing the
  apostrophe twice and deleting the first, or Find/Change.
- Measurements set with curly quotes: 6'2" must use **primes** (or, in informal contexts, straight marks are
  more acceptable than curly). Primes are often slanted straight strokes.

## Languages differ
- English US: "double" outer, 'single' inner; UK often 'single' outer.
- German: „low-high" or »guillemets pointing in«. French: « guillemets with spaces » (narrow non-breaking spaces).
- Swiss: «no spaces». Set the paragraph **Language** in InDesign - with Use Typographer's Quotes on and the
  Dictionary preferences' double/single quote choices per language, InDesign uses the right ones.

## Fixing copy
- InDesign: Preferences > Type > **Use Typographer's Quotes**; when placing Word files tick it in Import Options.
- Find/Change: with Use Typographer's Quotes on, find `"` and change to `"` (and the same for `'`) - InDesign
  resolves the direction of each replacement quote.
- Check after: `(?<=\s)'(?=\d)` finds quotes before years that should be apostrophes.
- Web: author with real characters (UTF-8); CMSs like WordPress "smartypants" convert, but code blocks must stay straight.

## Verify
- [ ] Find `"` and `'` (straight) in body text returns nothing except intended code/measurements.
- [ ] Abbreviation apostrophes point the right way; quotes match the language.
