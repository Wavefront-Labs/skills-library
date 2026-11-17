---
id: computing-software.database-administration.duckdb.duckdb-sample
name: duckdb-sample
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, sample, tablesample, reservoir, bernoulli, system-sampling]
level: practitioner
status: docs-checked
description: "Pick random subsets in DuckDB with USING SAMPLE or TABLESAMPLE: reservoir, bernoulli and system methods, seeds, row counts versus percentages, and sampling before or after a join."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/sample.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/samples.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query a random subset fast, with the right sampling method.

Size is a percentage (`10%` or `10 PERCENT`) or fixed rows (`10` or `10 ROWS`). Defaults: `reservoir` for a row count, `system` for a percentage.

```sql
SELECT * FROM tbl USING SAMPLE 5;                         -- exactly 5 rows, reservoir
SELECT * FROM tbl USING SAMPLE 10%;                       -- approx 10%, system
SELECT * FROM tbl USING SAMPLE 10 PERCENT (bernoulli);
SELECT * FROM tbl USING SAMPLE 10 PERCENT (reservoir);    -- exactly 10% up to rounding
SELECT * FROM tbl USING SAMPLE reservoir(50 ROWS) REPEATABLE (100);
SELECT * FROM tbl USING SAMPLE 20% (system, 377);         -- method, seed
```

Methods:
- `reservoir`: exact size, the only method supporting a fixed row count. Materialises the whole sample in memory and shares a reservoir across threads, so avoid large samples and percentages.
- `bernoulli`: percentage only; each row independently, so the count varies. No multi-thread penalty.
- `system`: each vector (cluster) is included with the percentage chance; more efficient than bernoulli but variance is `vectorSize` times higher. Not suitable below about 10k rows (you can get all or none of the rows even at 50 PERCENT); use `bernoulli` there.

Seeds: samples differ between runs unless a seed is given, and a seed only guarantees repeatability when `SET threads = 1`.

Join placement: `USING SAMPLE` samples after the entire FROM clause has been resolved (the clause page says right after anything in FROM, so after joins but before the WHERE clause or any aggregates). `TABLESAMPLE` samples directly from its own table, which matters with joins:

```sql
SELECT * FROM tbl TABLESAMPLE reservoir(20%), tbl2 WHERE tbl.i = tbl2.i;   -- before join
SELECT * FROM tbl, tbl2 WHERE tbl.i = tbl2.i USING SAMPLE reservoir(20%);  -- after join
```
`TABLESAMPLE` is essentially equivalent to a subquery `(SELECT * FROM tbl USING SAMPLE reservoir(20%)) tbl`.

## Checked

2026-11-07. Read the DuckDB 1.4 docs pages sql/samples.md and sql/query_syntax/sample.md in full. Confirmed: size forms, default methods, every example including seeds and `REPEATABLE`, reservoir/bernoulli/system behaviour and cautions, the seed and `SET threads = 1` caveat, the 10k-row warning, TABLESAMPLE versus USING SAMPLE and the subquery equivalence. Changed: reworded the join placement paragraph to the pages' wording (the two pages phrase the WHERE ordering differently), softened "fastest" for system sampling to "more efficient than bernoulli", removed the invented Verify step.

Method: documentation only; no commands were run.
