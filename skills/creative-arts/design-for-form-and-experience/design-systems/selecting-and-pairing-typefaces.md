---
id: creative-arts.design-for-form-and-experience.design-systems.selecting-and-pairing-typefaces
name: selecting-and-pairing-typefaces
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [font-pairing, typeface-selection, typeface-pairing, type-pairing, font-selection, typography]
level: practitioner
status: draft
description: "Select and pair typefaces: define voice and function, test legibility and language support, pair by contrast and shared structure, limit families and check licences."
sources:
  - "Robert Bringhurst, The Elements of Typographic Style"
  - "Ellen Lupton, Thinking with Type (Princeton Architectural Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Typeface selection and pairing

## Select
1. **Define the role:** UI text at small sizes, headlines, data tables, long reading.
2. **Match the brand voice** with the typeface's character, but legibility comes first for UI.
3. **Legibility checks:** clear letterforms at 12-16 px (distinguish I, l, 1, O, 0), generous x-height, open apertures, tabular figures available (see `...interaction-design.using-tabular-figures-for-numbers`).
4. **Coverage:** needed languages and scripts, diacritics, symbols, weights (at least regular, medium or semibold, bold), italics, and a variable font option.
5. **Licence and delivery:** web-font licence, self-hosting rights, file size (see `...design-systems.loading-web-fonts-without-layout-shift`).
6. **System fonts** (system-ui) are a legitimate choice: fast and native.

## Pair
- **One family** with multiple weights is often enough (a superfamily with sans and serif versions pairs naturally).
- **Contrast with a reason:** pair a serif headline with a sans body, or a geometric display face with a humanist text face; make them clearly different, not almost the same.
- **Share structure:** similar x-height, proportions or stroke contrast helps them sit together.
- **Limit to two families** (plus a monospace for code if needed).
- **Assign roles** (display, text, UI, code) and encode them as tokens.
- **Test** with real content, in all sizes and at weights used, in light and dark mode.

## Verify
- [ ] Every role has one named face and weights.
- [ ] Required languages render without fallback.
- [ ] The licence covers web, app and embedding as used.
