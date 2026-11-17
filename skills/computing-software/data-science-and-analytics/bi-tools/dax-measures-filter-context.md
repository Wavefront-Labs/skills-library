---
id: computing-software.data-science-and-analytics.bi-tools.dax-measures-filter-context
name: dax-measures-filter-context
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [dax-measures, filter-context, calculate-function, pbi-dax]
level: practitioner
status: docs-checked
description: "Create explicit measures with SUM, DIVIDE and CALCULATE and reason about filter context versus row context."
sources:
  - https://learn.microsoft.com/dax/calculate-function-dax
  - https://learn.microsoft.com/dax/divide-function-dax
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAX basics
```dax
Total Sales = SUM ( Sales[Amount] )
Margin % = DIVIDE ( [Total Profit], [Total Sales] )
Sales EU = CALCULATE ( [Total Sales], Customer[Region] = "EU" )
Sales All Regions = CALCULATE ( [Total Sales], REMOVEFILTERS ( Customer[Region] ) )
```
## Gotchas
- CALCULATE adds a filter for columns not yet in the filter context and overwrites existing filters on columns that are; wrap a filter in KEEPFILTERS to add it without removing existing filters on the same columns.
- A Boolean filter argument can reference columns of a single table only, cannot reference measures and cannot use a nested CALCULATE; use a table filter such as FILTER for those cases.
- CALCULATE with no filters turns row context into filter context (context transition), needed for an expression evaluated in a calculated column or iterator; using a model measure in row context does this automatically.
- ALL also works as a filter modifier, but Microsoft recommends REMOVEFILTERS where supported.
- DIVIDE returns BLANK() on division by zero, or an alternate result (a constant) passed as the third argument.
- CALCULATE is not supported in DirectQuery mode inside calculated columns or RLS rules.
## Verify
- [ ] Put the measure in a table by the filter column and check the sub-totals against the source.

## Checked
Confirmed on the CALCULATE page: syntax, filter overwrite versus add behaviour, KEEPFILTERS, REMOVEFILTERS/ALL guidance, Boolean filter rules, context transition, and the DirectQuery calculated-column/RLS restriction. Confirmed on the DIVIDE page: BLANK() default, alternate result as a constant. Removed: the statement that calculated columns evaluate at refresh and measures at query time (not on the cited pages) and the "intersect" wording. Replaced ALL with REMOVEFILTERS in the example (ALL kept as a note).
Method: docs-checked 2026-11-09 against the CALCULATE and DIVIDE pages on Microsoft Learn, both read in full.
