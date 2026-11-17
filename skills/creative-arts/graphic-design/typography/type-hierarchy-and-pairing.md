---
id: creative-arts.graphic-design.typography.type-hierarchy-and-pairing
name: type-hierarchy-and-pairing
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, type, typeface, font-pairing, type-hierarchy, type-scale, hierarchy-variables, modular-scale, leading, line-height, measure, line-length, tracking, letter-spacing, kerning, x-height, serif, sans-serif, web-typography, print, google-fonts, variable-fonts, readability, legibility]
level: practitioner
status: draft
description: "Set readable, hierarchical type: pick one or two families, build a size scale, set measure and leading, separate levels with few variables, and pair typefaces by shared structure."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type hierarchy and pairing — readable first, then expressive

**Goal:** text where the reader knows in one glance what to read first, second and
third, and can read the body for long stretches without effort.

## 1. Start with the body text
Everything else is relative to it.
- **Size:** screen body text commonly 16–20 px; print body commonly 9–12 pt depending
  on typeface and audience. Typefaces with a large x-height look bigger at the same size —
  judge by eye, not by number.
- **Measure (line length):** roughly 45–75 characters per line including spaces;
  ~66 is a frequently cited ideal. Too long and readers lose the next line; too short and
  rhythm breaks.
- **Leading (line height):** around 1.3–1.6× size for body. Longer lines need more;
  large display type needs less (often 1.0–1.2).
- **Alignment:** flush left / ragged right is safest. Justified text needs hyphenation
  and a good composer (InDesign's Paragraph Composer) or it produces rivers of space.

## 2. Build a scale
Pick a ratio and generate sizes from the body size — e.g. ratio 1.25 from 16 px: 16,
20, 25, 31, 39, 49. Popular ratios: 1.125–1.2 for dense UI, 1.25–1.333 for documents,
1.5+ for expressive editorial. Use **only** scale sizes. Fewer sizes, clearer hierarchy.

## 3. Separate levels with as few variables as possible
Variables: size, weight, case, colour, spacing, style (italic), typeface.
- Change **one or two** variables per level. Large + bold + red + caps for a heading
  is shouting; size + weight alone usually suffices.
- **Space is hierarchy:** more space above a heading than below it ties the heading to
  its content. Equal space above and below makes headings float.
- Test with the **squint test** or blur the layout: the levels should still read in order.

## 4. Pairing typefaces
- **One family is often enough.** A superfamily with many weights (and maybe a serif
  and sans version) gives contrast without conflict.
- When pairing two, aim for **contrast in role, harmony in structure**: e.g. a serif
  for body with a sans for headings, sharing similar proportions or x-height.
- Avoid pairing two typefaces that are *similar but not the same* (two geometric sans
  serifs) — it reads as a mistake.
- Assign roles strictly: typeface A for headings, B for body and UI. Don't mix within a level.
- Check the full character set you need (accents, numerals, currency, small caps,
  tabular figures for tables).

## 5. Spacing details
- **Track** (letter-space) all-caps and small text slightly looser (+5 to +10% / 50–100
  units in Adobe apps); tighten very large display type slightly.
- **Kern** display type by eye — optical kerning helps for problem pairs (AV, To, Ty)
  but check headlines manually.
- Use real typographic characters: curly quotes ‘ ’ “ ”, apostrophe ’, en dash –
  for ranges, em dash — for breaks, true ellipsis or spaced periods consistently.

## Gotchas
- **Faux bold/italic** (software-generated) look wrong; install real weights.
- **Licensing:** desktop, web, app and broadcast use are often separate font licences.
  Check before delivery; Google Fonts are mostly under the SIL Open Font License.
- **Web fonts and fallback:** set a similar system fallback to limit layout shift.
- **Light weights on screens** and thin type over images fail contrast; check WCAG
  contrast (4.5:1 for normal body text).
- Ranges above are widely taught conventions, not hard rules; trust a printed proof or
  device test over numbers.

## Verify
- [ ] Body text measure is ~45–75 characters with comfortable leading on the real medium.
- [ ] All sizes come from one scale; no more than ~5 used.
- [ ] Each level differs by one or two variables; blur test shows the right order.
- [ ] At most two families, with defined roles.
- [ ] Real quotes/dashes, no faux styles, font licence covers the use.
