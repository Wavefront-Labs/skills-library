---
id: creative-arts.design-for-form-and-experience.interaction-design.using-tabular-figures-for-numbers
name: using-tabular-figures-for-numbers
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [tabular-figures, tabular-nums, numerals, ui-typography, data-tables, font-features, opentype]
level: practitioner
status: draft
description: "Use tabular (monospaced) figures for numbers in tables, prices and timers so digits align and do not jitter, with font-variant-numeric and right alignment."
sources:
  - "MDN Web Docs - font-variant-numeric (developer.mozilla.org/docs/Web/CSS/font-variant-numeric)"
  - "Butterick's Practical Typography - Numbers (practicaltypography.com/numbers.html)"
  - "Inter typeface features - tnum, case, zero (rsms.me/inter)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tabular figures

**Goal:** numbers in columns line up, and changing values do not make the layout jump.

## Concepts
- **Proportional figures** give each digit its own width ("1" narrower than "8"): good in running text.
- **Tabular figures** make all digits the same width: needed in tables, financial values, scoreboards, timers, counters, code.
- **Lining vs oldstyle:** lining figures sit on the cap height (UI default); oldstyle in running prose only.

## CSS
```css
.num, td.number, .timer { font-variant-numeric: tabular-nums; }
/* also useful: */ font-variant-numeric: tabular-nums slashed-zero; /* distinguish 0 and O */
font-feature-settings: "tnum" 1; /* older fallback */
```
- Not every font supports it: check for `tnum` (Inter, Roboto, SF Pro, IBM Plex, Source Sans do); otherwise use a monospaced font for the numeric cells.
- Web font subsetting can strip OpenType features; keep `tnum` in the subset.

## Layout rules
1. **Right-align numeric columns** (or align on the decimal point); left-align text columns. Headers align with their data.
2. Same decimal places in a column; thousands separators and units in the header, not repeated per cell.
3. Use tabular figures also for **live-updating values** (stock price, countdown) so width stays steady.
4. Negative numbers: use a true minus sign (U+2212) rather than hyphen and consider parentheses for accounting.
5. Use locale-aware formatting (`Intl.NumberFormat`).

## Verify
- [ ] Numeric columns right-aligned with tabular-nums.
- [ ] Live counters do not shift width as digits change.
- [ ] Font supports `tnum` after subsetting.
