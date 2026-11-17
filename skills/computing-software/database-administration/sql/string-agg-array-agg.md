---
id: computing-software.database-administration.sql.string-agg-array-agg
name: string-agg-array-agg
category: computing-software
field: database-administration
product: sql
tags: [sql, string-agg-array-agg]
level: practitioner
status: docs-checked
description: "Concatenate or collect grouped values with string_agg, array_agg and group_concat."
sources: ["https://www.postgresql.org/docs/current/functions-aggregate.html", "https://www.sqlite.org/lang_aggfunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# string_agg array_agg and group_concat

- PostgreSQL: `string_agg(name, ', ' ORDER BY name)` concatenates the non-null input values, preceding each value after the first with the delimiter (if the delimiter is not null). `array_agg(x ORDER BY y)` collects all input values into an array, including nulls.
- PostgreSQL aggregates accept an ORDER BY clause only where the output depends on ordering, so `string_agg`, `array_agg` and `json_agg` take it.
- SQLite: `group_concat(X, Y)` concatenates all non-NULL values of X, with `,` as separator if Y is omitted. `string_agg(X, Y)` is an alias for it, compatible with PostgreSQL and SQL Server; `group_concat` is compatible with MySQL. An ORDER BY goes immediately after the last parameter inside the call.
- Without an ORDER BY inside the aggregate, the input order is arbitrary and can change from one run to the next (SQLite page). Treat PostgreSQL the same way.
- Gotcha: `array_agg` keeps NULLs but `string_agg` and `group_concat` skip them. Use `array_agg(x) FILTER (WHERE x IS NOT NULL)` or `COALESCE` when you need a specific behaviour.
- Self-check: insert rows in a different order and compare the output with and without the inner ORDER BY.

## Checked

2026-11-08. Confirmed against the PostgreSQL Aggregate Functions page and the SQLite Aggregate Functions page. Removed: the claim that all NULL inputs are skipped (array_agg includes nulls), the all-NULL-group result, the SQLite 3.44 version gate, and the MySQL group_concat_max_len and SQL Server WITHIN GROUP statements, none of which these pages cover. The FILTER (WHERE ...) aggregate syntax is confirmed on the Value Expressions page (https://www.postgresql.org/docs/current/sql-expressions.html).

Method: documentation only; no commands were run.
