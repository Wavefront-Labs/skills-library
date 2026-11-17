---
id: mathematics.applied-data-analysis-and-visualization.tableau.calculated-fields-and-lod-expressions
name: calculated-fields-and-lod-expressions
category: mathematics
field: applied-data-analysis-and-visualization
product: tableau
tags: [tableau, tableau-desktop, tableau-public, calculated-field, lod-expression, level-of-detail, fixed, include, exclude, table-calculation, window-sum, running-total, percent-of-total, order-of-operations, context-filter, aggregation, attr, countd, granularity, viz-level-of-detail, dashboard, power-bi, dax, data-visualization, data-analysis]
level: practitioner
status: draft
description: "Write Tableau calculations that compute at the intended level: row vs aggregate calcs, FIXED/INCLUDE/EXCLUDE LOD expressions, table calcs, and the filter order of operations that changes results."
sources: ["Tableau Help: Create Level of Detail Expressions", "Tableau Help: Tableau's Order of Operations", "Tableau Help: Transform Values with Table Calculations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calculated fields and LOD expressions in Tableau

**Goal:** get numbers in a Tableau view that mean what you think — most Tableau errors
are calculations evaluated at the wrong level of detail or after the wrong filter.

## 1. Know the view's level of detail
The **viz LOD** is the set of dimensions on Rows, Columns, Marks (Detail, Colour, etc.).
Every aggregate is computed per combination of those dimensions. Adding a dimension to
Detail changes every number in the view. Ask "one mark = what?" before writing a calc.

## 2. Row-level vs aggregate calculations
- Row-level: `[Sales] - [Cost]` — computed per data row, then aggregated (SUM by default).
- Aggregate: `SUM([Profit]) / SUM([Sales])` — a ratio of totals. Writing
  `[Profit]/[Sales]` and letting Tableau SUM it adds up per-row ratios — wrong.
- You can't mix: `[Sales] / SUM([Sales])` errors ("cannot mix aggregate and
  non-aggregate"). Use an LOD or a table calc instead.
- `COUNTD([Customer ID])` for distinct counts; `ATTR([Field])` returns the value if unique
  in the mark, `*` otherwise — a quick granularity check.
- Integer division: `INT` fields divide as integers in some data sources; wrap with
  `FLOAT()` if a ratio comes back as 0.

## 3. LOD expressions
Compute at a level independent of (or relative to) the view:
- **FIXED:** `{ FIXED [Customer ID] : MIN([Order Date]) }` — first purchase date per
  customer, regardless of what's in the view. Use for cohorts, customer-level metrics,
  percent-of-total with `{ FIXED : SUM([Sales]) }` (grand total).
- **INCLUDE:** `{ INCLUDE [Order ID] : SUM([Sales]) }` then AVG in the view = average order
  value per region, computed at order level then averaged.
- **EXCLUDE:** `{ EXCLUDE [Month] : SUM([Sales]) }` — total for the year shown alongside
  each month, for share-of-year.
- Cohort pattern: `DATETRUNC('month', { FIXED [Customer ID] : MIN([Order Date]) })` as a
  dimension, then COUNTD of customers by order month = retention matrix.
- FIXED results behave like dimensions when not aggregated; INCLUDE/EXCLUDE results are measures.

## 4. Table calculations
Computed on the aggregated table in the view: running totals, `WINDOW_SUM`, ranks,
percent of total, difference from previous.
- Always set **Compute Using / Edit Table Calculation** explicitly (Table across, Pane down,
  or specific dimensions). The default often isn't what you meant.
- `SUM([Sales]) / TOTAL(SUM([Sales]))` = share of the table/partition.
- Table calcs only see marks that survive filtering — filtering the view changes the
  denominator.

## 5. Order of operations (why filters change results)
Approximate order: extract filters → data source filters → **context filters** →
**FIXED LOD** → dimension filters → INCLUDE/EXCLUDE LOD → measure filters →
**table calculations** → table-calc filters.
Consequences:
- A normal dimension filter does **not** affect FIXED — add the filter to context
  (right-click › Add to Context) if FIXED should respect it.
- To hide marks but keep them in a running total or percent-of-total, filter with a table
  calc such as `LOOKUP(ATTR([Category]),0)` instead of a dimension filter.

## 6. Check your numbers
Build a plain crosstab (Text table) of the same measure, or `Analysis › View Data`, and
compare against a known total from the source (SQL or Excel). Use `ATTR` and `COUNTD`
to confirm the granularity you assumed.
Power BI users: FIXED ≈ DAX `CALCULATE(..., ALLEXCEPT(...))`; the mental model of
evaluation context is similar.

## Uncertainty notes
Order of operations summarised from Tableau's help page as I recall it; minor items
(sets, Top N) are omitted — check the current diagram. Integer-division behaviour depends
on data source and version.

## Verify
- [ ] You can state what one mark represents in each sheet.
- [ ] Ratios are aggregate calcs (`SUM/SUM`), not summed row ratios.
- [ ] Each LOD's type (FIXED/INCLUDE/EXCLUDE) is justified and filter interaction checked.
- [ ] Every table calc has explicit Compute Using.
- [ ] Key totals reconcile to the source outside Tableau.
