---
id: computing-software.database-administration.sql.sql-aggregates-group-by-having
name: sql-aggregates-group-by-having
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-aggregation, group-by, having, count-distinct, aggregate-nulls]
level: practitioner
status: docs-checked
description: "Aggregate correctly with GROUP BY, HAVING, DISTINCT and NULL behaviour of COUNT, SUM and AVG."
sources: ["https://www.postgresql.org/docs/current/functions-aggregate.html", "https://www.postgresql.org/docs/current/queries-table-expressions.html", "https://www.sqlite.org/lang_aggfunc.html", "https://www.sqlite.org/lang_select.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aggregates and GROUP BY

- `COUNT(*)` counts rows; `COUNT(col)` counts rows where `col` is not NULL; in SQLite `count(DISTINCT x)` counts distinct non-NULL values (any single-argument aggregate accepts `DISTINCT`).
- PostgreSQL: except for `count`, aggregates return NULL when no rows are selected. `SUM` of no rows is NULL, not zero, and `array_agg` gives NULL rather than an empty array; wrap with `COALESCE(SUM(x), 0)`. SQLite behaves the same for `sum()` (the SQL standard requires it) and adds a non-standard `total()` that returns 0.0.
- `SUM`, `AVG`, `MIN` and `MAX` use only non-NULL inputs. PostgreSQL `avg(integer)` returns `numeric`; SQLite `avg()` always returns a floating point value.
- SQLite `sum()` raises an "integer overflow" error if all inputs are integers and the total overflows; `total()` never does. For wildly different float magnitudes the sum can be imprecise.
- Every non-aggregated SELECT column must appear in `GROUP BY` or be functionally dependent on it. PostgreSQL accepts grouping by the primary key alone, because the other columns of that table are then functionally dependent.
- SQLite does not enforce this: a "bare" column in an aggregate query takes its value from one input row of the group, usually undefined. The exception is a query with exactly one built-in `min()` or `max()`, where bare columns come from the row holding the min or max (an arbitrary one of them on ties). Treat bare columns as a bug source.
- `HAVING` eliminates groups after grouping and may reference aggregates; `WHERE` filters rows before grouping, so put row-level conditions in `WHERE`. With aggregates but no `GROUP BY`, the result is a single group row, and a `HAVING` without aggregates or `GROUP BY` also forms one group.
- Conditional aggregation in SQLite: a `FILTER (WHERE ...)` clause on the aggregate includes only rows for which the expression is true. Portable alternative: `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`.
- Ordering: aggregates whose result depends on input order (`string_agg`, `array_agg`, `json_agg`, SQLite `group_concat` and `string_agg`) are in arbitrary order unless you write `ORDER BY` inside the call, e.g. `string_agg(x, ',' ORDER BY x)`. SQLite `string_agg(X,Y)` is an alias of `group_concat(X,Y)`; the default separator is a comma.
- Medians: PostgreSQL `percentile_cont(0.5) WITHIN GROUP (ORDER BY x)` interpolates between adjacent values. SQLite has `median(X)`, `percentile_cont(Y,P)` and `percentile_disc(Y,P)` only from 3.51.0 when compiled with `-DSQLITE_ENABLE_PERCENTILE`, or as a loadable extension in earlier versions.
- PostgreSQL `count(*)` over a whole table takes effort proportional to table size (a scan of the table or an index covering all rows).

## Checked

2026-11-08. Read: PostgreSQL 9.21 Aggregate Functions (general-purpose table, NULL note, ordering note, count note, ordered-set `percentile_cont` row), PostgreSQL 7.2.3 GROUP BY and HAVING, SQLite built-in aggregate functions (all), SQLite SELECT section 2.5 bare columns. Removed unconfirmed claims: SQL Server integer-average truncation, MySQL `ONLY_FULL_GROUP_BY`, version numbers for SQLite `FILTER` and SQL Server `STRING_AGG`, the `LISTAGG`/`GROUP_CONCAT` dialect list for MySQL and Oracle, and "grouping includes NULL as one group". PostgreSQL `FILTER` syntax (section 4.2.7) was not read, so it is not claimed.
Method: documentation only; no commands were run.
