---
id: computing-software.database-administration.duckdb.duckdb-join-types
name: duckdb-join-types
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, join, semi-join, anti-join, positional-join, lateral, natural-join, self-join]
level: practitioner
status: docs-checked
description: "Choose among DuckDB join forms: outer, cross, USING, NATURAL, SEMI, ANTI, LATERAL, POSITIONAL and self-joins, with their null and alias gotchas."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/from.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right join keyword. (ASOF is in `duckdb-asof-join`.)

- Outer: `LEFT`, `RIGHT`, `FULL` keep unpaired rows, filling the other side with NULL; anything not OUTER is INNER.
- Cross: `a CROSS JOIN b` equals `FROM a, b`.
- Conditional: `JOIN r ON (n_regionkey = r_regionkey)`; any predicate works, not just equality. `JOIN r USING (regionkey)` when the column names match.
- Natural: `city_airport NATURAL JOIN airport_names` joins on shared column names (here `iata`).
- Semi: `SEMI JOIN ... USING (iata)` returns left rows with at least one match; same logic as `IN`. Anti: `ANTI JOIN` returns left rows with no match; like `NOT IN` except NULLs from the right table are ignored. Neither returns more rows than the left table.

```sql
SELECT * FROM city_airport SEMI JOIN airport_names USING (iata);
SELECT * FROM city_airport ANTI JOIN airport_names USING (iata);
```

- Lateral: a FROM subquery may refer to earlier items; generalises correlated subqueries and may return several rows per input. `FROM range(3) t(i), LATERAL (SELECT i + 1) t2(j);` DuckDB detects when LATERAL is needed, so the keyword is optional.
- Positional: `t1 POSITIONAL JOIN t2` pairs rows by physical order and is always FULL OUTER (length of the longer input, NULL fill). Useful for data frames, CSV or Parquet files.
- Self-join needs aliases: `SELECT * FROM t JOIN t USING(x)` gives `Binder Error: Duplicate alias "t" in query!`; use `t AS t1 JOIN t AS t2 USING(x)`.
- Shorthands: rename columns inline, `t1 NATURAL JOIN t2 t2(x)`, or join literal rows, `NATURAL JOIN (VALUES (2), (4)) _(x)`.

## Checked

2026-11-07. Read the FROM and JOIN Clauses page and confirmed outer, cross, conditional, USING, NATURAL, SEMI/ANTI, LATERAL (keyword optional), POSITIONAL (always FULL OUTER), self-join alias error text and the two shorthands. Removed the Verify step, which the page does not state.

Method: documentation only; no commands were run.
