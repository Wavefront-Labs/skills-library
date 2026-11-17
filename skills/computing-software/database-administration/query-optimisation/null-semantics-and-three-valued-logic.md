---
id: computing-software.database-administration.query-optimisation.null-semantics-and-three-valued-logic
name: null-semantics-and-three-valued-logic
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, three-valued-logic, is-distinct-from, null-handling, coalesce, sql-fluency]
level: practitioner
status: gated
description: "Reason correctly about SQL NULLs: three-valued logic in WHERE, NULL-safe comparison (IS DISTINCT FROM, <=>), COALESCE, aggregates, NOT IN traps and indexing effects."
sources:
  - https://www.postgresql.org/docs/current/functions-comparison.html
  - https://modern-sql.com/concept/null
  - https://dev.mysql.com/doc/refman/8.4/en/working-with-null.html
  - https://www.postgresql.org/docs/current/queries-order.html
  - https://www.postgresql.org/docs/current/sql-createtable.html
  - https://learn.microsoft.com/en-us/sql/t-sql/queries/is-distinct-from-transact-sql
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Nulls.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NULL semantics and three-valued logic

## The rules
- Any comparison with NULL (`=`, `<>`, `<`) yields **UNKNOWN**, not true/false. WHERE keeps only TRUE rows.
- `NOT UNKNOWN` is UNKNOWN. So `WHERE NOT (status = 'x')` also drops rows where status is NULL.
- `TRUE OR UNKNOWN` = TRUE; `FALSE AND UNKNOWN` = FALSE; others propagate UNKNOWN.

```sql
SELECT count(*) FROM users WHERE country <> 'AU';                 -- excludes NULL countries
SELECT count(*) FROM users WHERE country IS DISTINCT FROM 'AU';   -- includes them
```

## NULL-safe comparison
| Engine | Syntax |
|---|---|
| Standard / PostgreSQL / SQL Server 2022+ / SQLite (`IS`) | `a IS DISTINCT FROM b`, `a IS NOT DISTINCT FROM b` |
| MySQL / MariaDB | `a <=> b` |
| Oracle | `DECODE(a, b, 0, 1) = 0` or explicit `(a = b OR (a IS NULL AND b IS NULL))` |

Change detection in upserts/ETL: `WHERE t.col IS DISTINCT FROM s.col` updates only changed rows, including NULL ↔ value transitions that `<>` misses.

## NOT IN with NULLs
```sql
SELECT * FROM a WHERE a.id NOT IN (SELECT b.a_id FROM b);   -- returns nothing if any b.a_id IS NULL
```
Use `NOT EXISTS`.

## Aggregates
- `count(*)` counts rows; `count(col)` skips NULLs; `sum/avg/min/max` ignore NULLs; `sum` of no rows is NULL, not 0: `coalesce(sum(x), 0)`.
- `avg(col)` averages non-NULL values only; if NULL means 0 for your metric, `avg(coalesce(col, 0))`.
- GROUP BY and DISTINCT treat NULLs as one group.

## Functions
(All examples in this skill's SQL, including `IS DISTINCT FROM`, `NOT IN` with NULL, count/sum/avg, NULLIF and `||` with NULL, were run in DuckDB 1.5.6 and SQLite 3.50.4 with the results stated; sort order of NULLs differed: DuckDB last, SQLite first.)
`COALESCE(a, b, c)` first non-NULL; `NULLIF(x, 0)` turns 0 into NULL (avoid division by zero: `total / NULLIF(cnt, 0)`). String concatenation with `||` yields NULL if any part is NULL in standard SQL (Oracle treats `''` as NULL; MySQL `CONCAT` returns NULL, `CONCAT_WS` skips NULLs (gated: unconfirmed, source is paywalled or blocked)).

## Sorting and uniqueness
- NULLs sort last ascending in PostgreSQL (confirmed: nulls are treated as larger than any value) and Oracle (gated: unconfirmed, source is paywalled or blocked), first in MySQL (confirmed), SQL Server (lowest value, confirmed) and SQLite (run); specify `NULLS FIRST/LAST` where supported.
- UNIQUE constraints allow multiple NULLs (except SQL Server's unique index allows one NULL, confirmed in Microsoft docs; PostgreSQL 15+ `NULLS NOT DISTINCT` option).

## Verify
For any filter with `<>`/`NOT`, test with a row containing NULL in the column and confirm the intended behaviour.
