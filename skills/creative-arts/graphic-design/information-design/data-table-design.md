---
id: creative-arts.graphic-design.information-design.data-table-design
name: data-table-design
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, chart-design, data-visualisation, data-tables, table-design, number-alignment, tabular-numerals, row-rules, heatmap-table, sparklines-in-tables]
level: practitioner
status: draft
description: "Design data tables that are easy to scan: when a table beats a chart, number and text alignment, minimal rules, units and notes, and in-cell graphics."
sources:
  - https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data table design

**Goal:** tables where readers find a value, compare rows and see the pattern quickly.

## Table or chart?
Use a **table** when readers look up exact values, the dataset is small, values have different units, or the audience
needs precision (finance, specs). Use a **chart** when the shape (trend, distribution) is the message. Often both: chart
for the story, table in the appendix.

## Layout rules (Lupton's "data tables", Tufte's data-ink)
- **Align:** numbers right (or on the decimal, see decimal tab skill), text left, headers aligned like their column.
  Use **tabular lining figures**.
- **Few lines:** remove vertical rules; use light horizontal rules or alternating tints only where rows are long;
  a heavier rule under the header and above totals.
- **Whitespace** between columns separates them better than lines; group related columns with spanning headers.
- **Order rows** meaningfully (by value, by category, alphabetically for lookup) and say which.
- **Units and precision:** units in headers (`Revenue, $m`), consistent decimals (no more precision than meaningful),
  thousands separators. Use em dash or "n/a" consistently for missing values and explain in a note.
- **Totals** visually distinct (bold or rule above).
- **Highlight** the rows/cells the text discusses (bold, colour tint) - sparingly.

## Graphics inside tables
- **Heatmap** tint per cell (sequential palette) reveals patterns in big tables.
- **Sparklines** (tiny line charts) or in-cell bars add trend at a glance (Tufte's sparklines).

## Web and accessibility
Use real `<table>` markup with `<th scope>` headers and `<caption>`; responsive tables (scroll horizontally or stack
rows on mobile). In PDFs, tag header rows (see accessible PDF skill).

## Verify
- [ ] Numbers right/decimal aligned with tabular figures; minimal rules.
- [ ] Units, sources and notes present; sort order meaningful.
- [ ] A reader finds a specific value in a few seconds.
