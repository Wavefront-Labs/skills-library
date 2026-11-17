---
id: creative-arts.graphic-design.typography.true-small-caps
name: true-small-caps
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, typographic-details, punctuation, small-caps, all-small-caps, c2sc, smcp, acronyms, faux-small-caps, letterspacing]
level: intro
status: draft
description: "Use true small caps (OpenType smcp/c2sc) for acronyms, run-ins and labels instead of faux scaled capitals, with light letterspacing and correct setup in InDesign and CSS."
sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_pt#smcp
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-caps
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# True small caps

**Goal:** acronyms and small-cap text that match the weight and colour of the surrounding text.

## True vs faux
- **True small caps** are separate glyphs designed at about x-height with stroke weights matching lowercase.
- **Faux small caps** (software shrinks normal capitals, e.g. to 70%) are too thin and light - visibly wrong next to text.
- Check the font has them: OpenType menu in InDesign shows "All Small Caps" not bracketed; or the specimen.

## Where to use
- **Acronyms** in running text (NASA, BBC, UNESCO): all small caps keep them from shouting (Bringhurst).
  Some house styles keep full caps for acronyms - follow the style guide.
- **Run-in openings** (first words of a chapter in small caps).
- Labels, eyebrows, folios, running heads, AM/PM, era designations (BC, AD).

## Setting
- **InDesign:** Character panel > **All Small Caps** in the OpenType menu (uses `c2sc` + `smcp`) - converts both
  upper and lowercase to small caps. The Small Caps button in the Character panel uses real small caps if the font
  has them, else fakes them at the size set in Preferences > Advanced Type (70% default) - check.
- Automate acronyms with a GREP style `\b\u{2,}\b` -> character style `Small caps` (see GREP styles skill).
- **CSS:** `font-variant-caps: all-small-caps;` (both cases) or `small-caps;` (lowercase only). If the web font
  lacks them, browsers synthesise faux small caps - prefer `font-synthesis: none` and a font that has them.

## Spacing
Letterspace small caps slightly: +5 to +10% (InDesign tracking 50-100) so they do not look cramped (see
letterspacing capitals skill). Keep word spacing proportional.

## Gotchas
- Figures inside small-cap acronyms (G20, COVID-19): use oldstyle or small-cap figures if the font provides them.
- Copying text into another font without small caps falls back to faux or full caps.

## Verify
- [ ] Small caps match the stroke weight of lowercase at 400% zoom (no thin faux caps).
- [ ] Applied by style or GREP, consistently.
