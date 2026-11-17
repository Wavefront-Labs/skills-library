---
id: computing-software.database-administration.duckdb.duckdb-grouping-sets-rollup-cube
name: duckdb-grouping-sets-rollup-cube
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, grouping-sets, rollup, cube, grouping-id, subtotals]
level: advanced
status: docs-checked
description: "Compute subtotals and multi-dimension aggregates in DuckDB with GROUPING SETS, ROLLUP and CUBE, and tell super-aggregate NULLs from real NULLs using GROUPING_ID()."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/query_syntax/grouping_sets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: several GROUP BY levels in one query, with correct identification of subtotal rows. Not compatible with `GROUP BY ALL`.

```sql
SELECT city, street_name, avg(income) FROM addresses
GROUP BY GROUPING SETS ((city, street_name), (city), (street_name), ());   -- () = grand total
-- same four sets:
GROUP BY CUBE (city, street_name)
-- (city, street_name), (city), ():
GROUP BY ROLLUP (city, street_name)
```

- `ROLLUP (a, b, c)` yields (a,b,c), (a,b), (a), () : n+1 sets.
- `CUBE (a, b, c)` yields every combination, 2^n sets.
- Columns not in a given set come out as `NULL` in that set's rows. The result equals a `UNION ALL` of individual GROUP BY queries with `NULL AS col` placeholders.

Distinguishing NULLs: if grouped columns hold real NULLs (e.g. `students(course, type)` with NULL types), a NULL may be data or a roll-up marker. `GROUPING_ID(expr, ...)` (alias `GROUPING()`) is an aggregate returning BIGINT: 0 for ordinary rows, otherwise a bitfield where the first bit corresponds to the last argument, the second to the one before, etc., set when that expression is rolled up.

```sql
SELECT y, q, m, GROUPING_ID(y, q, m) AS "grouping_id()"
FROM days
GROUP BY GROUPING SETS ((y, q, m), (y, q), (y), ())
ORDER BY y, q, m;
-- (y,q,m) rows: 0; (y,q) rows: 1; (y) rows: 3; () row: 7
```

View the bits with `right(GROUPING_ID(y, q, m)::BIT::VARCHAR, 3)` (001, 011, 111). The arguments need not match the grouping sets in number or order, as long as each appears somewhere in the GROUPING SETS clause.

## Checked

2026-11-07. Read the GROUPING SETS page in full and confirmed the GROUP BY ALL incompatibility, the GROUPING SETS, CUBE and ROLLUP examples, n+1 and 2^n set counts, the NULL placeholders and UNION ALL equivalence, GROUPING_ID() and its GROUPING() alias, BIGINT result, the 0, 1, 3 and 7 values, the bitfield rule, the BIT cast display and the argument-independence note. Removed the Verify step.

Method: documentation only; no commands were run.
