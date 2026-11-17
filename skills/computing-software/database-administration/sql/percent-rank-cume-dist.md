---
id: computing-software.database-administration.sql.percent-rank-cume-dist
name: percent-rank-cume-dist
category: computing-software
field: database-administration
product: sql
tags: [sql, percent-rank-cume-dist]
level: advanced
status: docs-checked
description: "Compute relative position with PERCENT_RANK, CUME_DIST and percentile_cont."
sources: ["https://www.postgresql.org/docs/current/functions-window.html", "https://www.postgresql.org/docs/current/functions-aggregate.html", "https://www.sqlite.org/windowfunctions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PERCENT_RANK CUME_DIST and percentiles

- `percent_rank()` = (rank - 1) / (partition rows - 1), ranging 0 to 1 inclusive. `cume_dist()` = (partition rows preceding or peers with the current row) / partition rows, ranging 1/N to 1. Both need a window ORDER BY, and peers share the same value. SQLite documents both with the same meaning and says percent_rank returns 0.0 for a one-row partition.
- Ordered-set aggregates: `percentile_cont(0.5) WITHIN GROUP (ORDER BY v)` interpolates between adjacent inputs for a median; `percentile_disc` returns the first input value whose position in the ordering equals or exceeds the fraction. The fraction must be between 0 and 1 (error otherwise); a NULL fraction gives a NULL result.
- Ordered-set aggregates ignore NULL values in their aggregated input.
- SQLite's built-in window function list (row_number, rank, dense_rank, percent_rank, cume_dist, ntile, lag, lead, first_value, last_value, nth_value) has no percentile function.
- Self-check: median of 1,2,3,4 is 2.5 with cont and 2 with disc.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages functions-window.html and functions-aggregate.html and the SQLite windowfunctions.html page; the draft's Oracle and SQLite-extension remarks were dropped because the pages do not cover them.
