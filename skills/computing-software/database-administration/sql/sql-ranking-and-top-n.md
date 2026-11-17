---
id: computing-software.database-administration.sql.sql-ranking-and-top-n
name: sql-ranking-and-top-n
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-ranking, row-number-rank-dense-rank, ntile, top-n-per-group]
level: practitioner
status: docs-checked
description: "Rank rows with ROW_NUMBER, RANK, DENSE_RANK and NTILE and pick top N per group in PostgreSQL and SQLite."
sources: ["https://www.postgresql.org/docs/current/functions-window.html", "https://www.postgresql.org/docs/current/tutorial-window.html", "https://www.postgresql.org/docs/current/queries-limit.html", "https://www.sqlite.org/windowfunctions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ranking

- `row_number()` numbers rows in a partition from 1; rows tied on the window `ORDER BY` are numbered in an unspecified order, so add a tiebreaker column. `rank()` gives peers the same rank, with gaps (1,1,3); `dense_rank()` has no gaps (1,1,2); `ntile(n)` divides the partition into n buckets as equally as possible; `percent_rank()` is (rank - 1) / (rows - 1); `cume_dist()` is rows preceding or peers / total rows.
- Top N per group: `SELECT * FROM (SELECT *, row_number() OVER (PARTITION BY g ORDER BY score DESC, id) AS rn FROM t) x WHERE rn <= 3;`. Use `rank()` instead to keep tied rows.
- Window functions run after `WHERE`, `GROUP BY` and `HAVING` and are allowed only in the `SELECT` list and `ORDER BY`, so filter on a rank in an outer query (sub-select). A row removed by `WHERE` is never seen by the window function.
- The window `ORDER BY` does not order the output; give the query its own `ORDER BY` for a defined result order.
- Overall top N with no groups: `ORDER BY ... LIMIT n`. Always include `ORDER BY` with `LIMIT`, otherwise the subset is unpredictable; a large `OFFSET` is inefficient because skipped rows are still computed.
- SQLite supports the same `row_number()`, `rank()`, `dense_rank()`, `percent_rank()`, `cume_dist()` and `ntile()` window functions; with no window `ORDER BY`, all rows are peers and `rank()` / `dense_rank()` return 1.

## Checked

2026-11-08. Confirmed against the PostgreSQL 18 pages "Window Functions" (definitions of the ranking functions, peers), "Window Function Processing" tutorial (tie order, execution after WHERE/GROUP BY, sub-select filter), "LIMIT and OFFSET" (ORDER BY needed, large OFFSET) and the SQLite "Window Functions" page (row_number, rank, dense_rank, no-ORDER-BY behaviour). Removed as unconfirmed: `QUALIFY` support in Snowflake, BigQuery and DuckDB, the claim that an index on `(g, score DESC)` avoids sorting, and "ORDER BY LIMIT is cheaper than a window".
Method: documentation only; no commands were run.
