---
id: creative-arts.graphic-design.typography.lining-oldstyle-tabular-figures
name: lining-oldstyle-tabular-figures
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, typographic-details, punctuation, oldstyle-figures, tabular-figures, lining-figures, proportional-figures, font-variant-numeric, tnum, onum, numerals]
level: practitioner
status: draft
description: "Pick the right numeral style: oldstyle vs lining and proportional vs tabular figures for running text, headings, tables and UI, and set them in InDesign and CSS."
sources:
  - https://learn.microsoft.com/en-us/typography/opentype/spec/features_ko#tnum
  - https://developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lining, oldstyle, tabular and proportional figures

**Goal:** numbers that blend into text, align in tables and do not jitter in changing UI values.

## Two independent choices
| | **Proportional** (pnum) - widths vary | **Tabular** (tnum) - all digits same width |
|---|---|---|
| **Oldstyle** (onum) - ascend/descend like lowercase | running text in books, essays | rare: tables in text-heavy books |
| **Lining** (lnum) - cap height, uniform | headings, all-caps, UI labels | **tables, financial data, timers, prices in columns** |

- **Oldstyle figures** sit nicely in lowercase text (1990s, 3 pm) and avoid numbers SHOUTING in a paragraph.
- **Lining figures** suit capitals, headlines, and contexts with lots of numbers.
- **Tabular** figures align vertically in columns and keep counters/timers from shifting as digits change.
- The font's default varies: many text faces default to proportional oldstyle, many sans/UI faces to tabular lining.

## Setting them
- **InDesign:** Character panel menu > OpenType > Tabular Lining / Proportional Oldstyle / etc., or in character/
  paragraph styles (Basic Character Formats > OpenType Features > Figure Style). Put **Tabular Lining** in table styles.
- **Illustrator:** OpenType panel figure menu.
- **CSS:** `font-variant-numeric: tabular-nums lining-nums;` for tables and dashboards;
  `font-variant-numeric: oldstyle-nums proportional-nums;` for long-form body text. Older fallback:
  `font-feature-settings: "tnum" 1, "lnum" 1;`.
- **Slashed zero** (`zero`) for codes and data where 0/O confusion matters.

## Check font support
Not every font has all four styles. Check the specimen or the OpenType menu (bracketed = unsupported). Free UI
fonts like Inter, IBM Plex, Source Sans include tabular figures.

## Gotchas
- Mixing a font's oldstyle text figures with lining figures in headings of the same document is fine - by role, via styles.
- Tabular "1" can look gappy in running text - use proportional in paragraphs.
- Fractions and super/subscripts are separate features (frac, sups).

## Verify
- [ ] Table and price columns use tabular lining figures and align.
- [ ] Body text figure style chosen deliberately; numbers do not jump in live-updating UI.
