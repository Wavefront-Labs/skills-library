---
id: creative-arts.graphic-design.typography.ligatures
name: ligatures
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, typographic-details, punctuation, ligatures, standard-ligatures, discretionary-ligatures, liga, dlig, letterspacing-ligatures, font-variant-ligatures]
level: intro
status: draft
description: "Use standard ligatures (fi, fl, ff) by default, discretionary ligatures sparingly, and know when to disable them: tracked text, URLs, code and some languages."
sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_ko#liga
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-ligatures
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ligatures

**Goal:** letter combinations that do not collide, without ornamental ligatures where they distract.

## Types
- **Standard ligatures** (`liga`): fi, fl, ff, ffi, ffl - fix collisions (the f's hook hitting the i dot). On by default
  in InDesign (Character panel menu > Ligatures) and in browsers for most fonts. Keep them on for text.
- **Discretionary ligatures** (`dlig`): ct, st, Th, sp - decorative, period or calligraphic flavour. Display use only.
- **Contextual alternates** (`calt`): script fonts joining naturally; keep on for scripts.
- Historical ligatures (`hlig`): long s etc. - historical recreations.

## When to turn standard ligatures off
- **Letterspaced text** (tracking > ~+50 / 5%) - a ligature stays tight while other letters spread; InDesign
  automatically breaks ligatures beyond a tracking threshold only in some cases, so turn them off in letterspaced styles.
- **URLs, code, filenames, data** where each character must be distinct.
- **Monospaced fonts** for code: some coding fonts have "programming ligatures" (`!=`, `=>`) - a preference, off for teaching material.
- **Compound words across a morpheme boundary** in languages like German and Dutch (Auflage should not ligate f+l
  across "Auf|lage"): set the correct language in InDesign so hyphenation and ligature rules apply, or insert a
  zero-width non-joiner (U+200C) to break a ligature.
- Turkish dotless i: fi ligature can hide the dot distinction - many fonts handle it via `locl` if the language is set.

## Setting
- InDesign: in paragraph/character styles (Basic Character Formats > Ligatures; OpenType > Discretionary Ligatures).
- CSS: `font-variant-ligatures: common-ligatures;` (default), `no-common-ligatures;` for tracked labels,
  `discretionary-ligatures;` for display.

## Gotchas
- Searching PDFs: ligature glyphs can break text search/copy if the PDF lacks proper ToUnicode mapping - exporting
  from InDesign with current fonts is usually fine; test copy-paste.

## Verify
- [ ] No f/i collisions in body text; ligatures off in tracked caps and code.
- [ ] Discretionary ligatures only where intended.
