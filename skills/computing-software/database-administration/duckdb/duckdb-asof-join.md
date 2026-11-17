---
id: computing-software.database-administration.duckdb.duckdb-asof-join
name: duckdb-asof-join
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, asof-join, join, time-series, inequality, using]
level: advanced
status: docs-checked
description: "Match each row to the nearest earlier event in DuckDB with ASOF JOIN: required inequality, equality keys, ASOF LEFT, USING semantics and which column SELECT * returns."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/from.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: attach the nearest (first) matching reference event, such as the latest price at trade time.

```sql
SELECT t.*, p.price
FROM trades t
ASOF JOIN prices p
       ON t.symbol = p.symbol AND t.when >= p.when;
```

Rules:
- Needs at least one inequality on the ordering field: `>=`, `>`, `<=` or `<`, on any data type (most common is `>=` on a temporal type).
- All other conditions must be equalities (or `NOT DISTINCT`).
- Table order matters (left is the probe side, right the build side).
- Each left row joins at most one right row.
- Make it outer to keep unmatched rows: `ASOF LEFT JOIN` returns trades with NULL price when no earlier price exists (it can be specified as an OUTER join to find unpaired rows on either side).

USING form: the last column in the list must be the inequality, and it means `>=`:

```sql
SELECT * FROM trades t ASOF JOIN prices p USING (symbol, "when");
```
Gotcha: with `USING` and `SELECT *`, the ordering column returned comes from the left (probe) side, not the right (build) side. To see the price timestamp, list columns explicitly:

```sql
SELECT t.symbol, t.when AS trade_when, p.when AS price_when, price
FROM trades t ASOF LEFT JOIN prices p USING (symbol, "when");
```

Related: `duckdb-join-types` for other join kinds.

## Checked

2026-11-07. Read the FROM and JOIN Clauses page (As-Of Joins section) and confirmed the inequality rule, equality or NOT DISTINCT for other conditions, at most one right row per left row, OUTER/ASOF LEFT, the USING last-column `>=` rule and the left-side column returned by `SELECT *`. Removed the Verify step, which the page does not state.

Method: documentation only; no commands were run.
