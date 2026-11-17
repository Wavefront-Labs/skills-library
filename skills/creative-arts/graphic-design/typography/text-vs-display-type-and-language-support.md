---
id: creative-arts.graphic-design.typography.text-vs-display-type-and-language-support
name: text-vs-display-type-and-language-support
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, typeface-selection, font-pairing, text-vs-display-type, language-support, character-set, latin-extended, cyrillic, greek, glyph-coverage, optical-size]
level: practitioner
status: draft
description: "Choose typefaces by job: text faces for reading vs display faces for impact, optical sizes, and checking character sets for every language and symbol the project needs."
sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/os2#ur
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text vs display type and language support

**Goal:** typefaces that perform at their size and contain every character the content needs - checked before the design is approved.

## Text faces vs display faces
- **Text faces** are built for long reading at 8-14 pt / 14-20 px: moderate contrast, generous x-height and apertures,
  sturdy serifs/terminals, looser default spacing, full figure sets, italics, small caps.
- **Display faces** are built for 24 pt+: high contrast, tight spacing, distinctive details that look clumsy or break
  up at small sizes.
- **Optical sizes:** many families ship Caption / Text / Subhead / Display cuts, or a variable `opsz` axis. Use the
  cut that matches the size (Display cut for headlines; Text/Caption for body and notes).
- Using a display face for body text tires readers; using a text face huge can look heavy and loose - adjust tracking.

## Language and character support
List every language and special character in the project (brand names with accents, Polish, Turkish, Vietnamese,
Cyrillic, Greek, currency symbols, maths, arrows, fractions). Then check:
- Foundry specimen "language support" list; **Glyphs panel** in InDesign/Illustrator (Show: Entire Font); or tools
  like Wakamai Fondue / FontDrop for web fonts.
- Typical traps: Polish ogonek (ą ę), Romanian comma-below (ș ț vs cedilla), Turkish dotless ı and İ, Vietnamese
  stacked accents, Hungarian double acute (ő ű), €, ₹, ₺ and newer currency signs, Welsh ŵ ŷ.
- Missing glyphs show as pink highlights (InDesign) or fallback fonts (web) - a different design in the middle of a word.
- Non-Latin scripts (Arabic, Devanagari, CJK, Thai) need families designed for them; pair by structure and weight,
  and use the World-Ready composer (see composer skill).

## Process
1. Shortlist 3-5 families per role (text, display, UI).
2. Check licences for all uses (see font licensing skill).
3. Set real copy, in every language, at real sizes (see type testing skill).

## Verify
- [ ] Body face is a text face (or text optical size) and display face used only at display sizes.
- [ ] Every language and special character present in the chosen fonts - no fallbacks or pink highlights.
