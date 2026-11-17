---
id: computing-software.database-administration.sql.rollup-subtotals
name: rollup-subtotals
category: computing-software
field: database-administration
product: sql
tags: [sql, rollup-subtotals]
level: practitioner
status: docs-checked
description: "Produce hierarchical subtotals with GROUP BY ROLLUP."
sources: ["https://www.postgresql.org/docs/current/queries-table-expressions.html", "https://www.postgresql.org/docs/current/functions-aggregate.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ROLLUP subtotals and grand totals

- `GROUP BY ROLLUP (region, city)` yields groups (region, city), (region), and ().
- Mark subtotal rows with `GROUPING(city)` (1 when city is rolled up) rather than testing for NULL, which collides with real NULLs.
- Self-check: the sum of the detail rows equals the grand total row.

## Checked

2026-11-02. Confirmed in the PostgreSQL GROUPING SETS, CUBE and ROLLUP section and the GROUPING function entry (returns a bit mask of GROUP BY expressions not included in the current grouping set). Removed: the list of supporting engines and versions.
Method: documentation only; no commands were run.
