---
id: computing-software.data-science-and-analytics.bi-tools.power-query-transformations
name: power-query-transformations
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [power-query, query-folding, applied-steps]
level: practitioner
status: docs-checked
description: "Clean and reshape data with Power Query steps while preserving query folding so transformations push down to the source."
sources:
  - https://learn.microsoft.com/power-query/query-folding-basics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Power Query
- Every query has an M script; the Applied steps pane is a friendly view of it (for example Source, Navigation, Removed other columns, Sorted rows, Kept top rows). View the full script in the Advanced Editor (View tab, or Query group on the Home tab); editor changes update the script automatically.
- Query folding translates supported transformations into operations the data source performs; the rest run in the Power Query engine. Outcomes: full folding, partial folding or no folding.
- Structured sources with a query engine, such as SQL Server and OData Feed, commonly support folding. Sources without one, such as CSV and Excel files, do not.
- Folding after the Source step happens only when the connector and the transformation both support it. The engine may reorder steps during optimisation.
## Gotchas
- Check folding with View Native Query or View data source query where available (availability depends on the connector). In Power Query Online, use the query folding indicators next to applied steps and the query plan; those two are Online only.
- When several data sources are involved, each source's data privacy level is taken into account.
## Verify
- [ ] View Native Query (or the folding indicators in Power Query Online) confirms the steps expected to fold; row counts verified.

## Checked
Confirmed on the query folding basics page: M script and Applied steps, Advanced Editor location, folding definition and three outcomes, which sources fold, connector dependence, verification options and their Online-only limits, step reordering, privacy levels. Removed: the list of transformation steps, "put filters and column removal early", "setting types late breaks folding" and "merge on text keys is case sensitive", none of which the page states.
Method: docs-checked 2026-11-09 against the Microsoft Learn query folding basics page, read in full.
