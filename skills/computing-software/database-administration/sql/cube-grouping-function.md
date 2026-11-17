---
id: computing-software.database-administration.sql.cube-grouping-function
name: cube-grouping-function
category: computing-software
field: database-administration
product: sql
tags: [sql, cube-grouping-function]
level: advanced
status: docs-checked
description: "Aggregate over all dimension combinations with CUBE and label them with GROUPING."
sources: ["https://www.postgresql.org/docs/current/queries-table-expressions.html", "https://www.postgresql.org/docs/current/functions-aggregate.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CUBE and the GROUPING function

- `GROUP BY CUBE (a, b)` gives (a,b), (a), (b), ().
- `GROUPING(a, b)` returns a bit mask indicating which GROUP BY expressions are not included in the current grouping set; use in `CASE` for labels like 'All'.
- N columns produce 2^N grouping sets; keep to a few.
- Explicit alternative: `GROUPING SETS ((a), (b))`.
- Self-check: the row count equals the sum of distinct group counts per set.

## Checked

2026-11-02. Confirmed in the PostgreSQL GROUPING SETS, CUBE and ROLLUP section (CUBE (a, b, c) expands to all subsets, GROUPING SETS alternative) and the GROUPING function entry. Removed: nothing beyond rewording the GROUPING description.
Method: documentation only; no commands were run.
