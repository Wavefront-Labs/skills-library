---
id: computing-software.data-science-and-analytics.bi-tools.tableau-lod-expressions
name: tableau-lod-expressions
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [tableau-lod, fixed-lod, include-exclude-lod]
level: advanced
status: docs-checked
description: "Compute values at a different level of detail from the view with FIXED, INCLUDE and EXCLUDE, knowing when filters apply."
sources:
  - https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_lod.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LOD expressions
```
{ FIXED [Customer ID] : MIN([Order Date]) }      // first purchase date
{ FIXED : SUM([Sales]) }                         // table-scoped, same as {SUM([Sales])}
{ INCLUDE [Customer Name] : SUM([Sales]) }
{ EXCLUDE [Region] : SUM([Sales]) }
```
Structure: `{[FIXED | INCLUDE | EXCLUDE] <dimension declaration> : <aggregate expression>}`; separate several dimensions with commas.
## Gotchas
- FIXED ignores the dimensions in the view and ignores view filters other than context filters, data source filters and extract filters; add a dimension filter to context to make a FIXED expression respect it.
- INCLUDE adds dimensions to the view level of detail (useful for a dimension not in the view); fields based on it change as dimensions are added or removed. EXCLUDE subtracts dimensions from the view (percent of total, difference from overall average) and cannot be used in row-level expressions.
- The aggregate expression must be aggregated; ATTR is not supported and table calculations are not permitted. It may contain other LOD expressions (nested).
- Tableau cannot match a saved calculation's name to its contents: drag fields from the shelf into the declaration instead of typing, and do not exclude `YEAR([Order Date])` using a calculation named for it.
## Verify
- [ ] Check against a table-calc or SQL equivalent for one customer.

## Checked
Confirmed on the Tableau LOD page: syntax, FIXED/INCLUDE/EXCLUDE semantics and filter behaviour, table-scoped equivalence, aggregate expression rules, name-matching note. Removed: "INCLUDE/EXCLUDE respect view filters" (not stated), "LODs can be slow on large extracts" and the materialise advice, and the order-of-operations wording, replaced by the page's FIXED filter statement.
Method: docs-checked 2026-11-09 against the Tableau Help LOD expressions page, read in full.
