---
id: computing-software.database-administration.sql.sql-type-casting-and-conversion
name: sql-type-casting-and-conversion
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-type-casting, cast-function, implicit-conversion, parse-numbers]
level: practitioner
status: docs-checked
description: "Cast values explicitly in PostgreSQL and SQL Server, validate input before casting, and avoid implicit conversions that change results or defeat indexes."
sources: ["https://www.postgresql.org/docs/current/sql-expressions.html", "https://www.postgresql.org/docs/current/functions-info.html", "https://www.postgresql.org/docs/current/functions-formatting.html", "https://www.postgresql.org/docs/current/datatype-boolean.html", "https://www.postgresql.org/docs/current/datatype-numeric.html", "https://www.postgresql.org/docs/current/typeconv-overview.html", "https://learn.microsoft.com/en-us/sql/t-sql/functions/try-cast-transact-sql"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Casting

- Standard form `CAST(expression AS type)`. PostgreSQL also accepts `expression::type`, which its docs call
  historical PostgreSQL usage.
- SQL Server `TRY_CAST(expression AS data_type)` returns the value if the cast succeeds and NULL otherwise. A
  conversion that is explicitly not permitted (for example `int` to `xml`) still fails with an error, and the result
  of a string cast can depend on session settings such as `SET DATEFORMAT`.
- PostgreSQL `pg_input_is_valid(string text, type text)` returns true or false for whether a string is valid input for a
  type, for example `pg_input_is_valid('42000000000', 'integer')` is false. The docs say it only works as desired when
  the type's input function reports invalid input as a "soft" error; otherwise invalid input aborts the transaction
  as a plain cast would. Check the function's availability in your server version.
- PostgreSQL `to_number(text, text)` and `to_date(text, text)` parse formatted strings, for example
  `to_date('05 Dec 2000', 'DD Mon YYYY')`.
- PostgreSQL resolves operators and function calls by general rules on argument types, and its design principle is
  that implicit conversions should never have surprising or unpredictable outcomes. Still, match parameter types to
  column types so no conversion is needed. Other engines have their own implicit-conversion rules; check their docs
  and inspect the query plan for conversions on indexed columns.
- Boolean input in PostgreSQL accepts `true`, `yes`, `on`, `1` and `false`, `no`, `off`, `0`, case-insensitive,
  ignoring surrounding whitespace, and unique prefixes such as `t` or `n`. Validate user input before relying on it.
- `numeric` rounds ties away from zero, while `real` and `double precision` (on most machines) round ties to the
  nearest even number. Use `round()` explicitly rather than depending on cast behaviour.
- Clean data before casting: filter bad rows in an earlier step, or use `TRY_CAST` (SQL Server) or
  `pg_input_is_valid` (PostgreSQL). Do not assume a `WHERE` guard stops the cast being evaluated on other rows;
  confirm with the plan.

## Checked
2026-11-08. Confirmed in the PostgreSQL expressions page (`CAST` and `::`), system information functions page
(`pg_input_is_valid`, soft-error caveat), formatting functions page (`to_number`, `to_date`), Boolean and numeric
type pages, type-conversion overview (design principle) and the Microsoft Learn TRY_CAST page. Removed: the claim
that `'abc' = 0` is true in MySQL (the MySQL manual returned 403), SQL Server precedence examples with `varchar_col`
and `N'x'`, the PostgreSQL 16 version tag, the `OFFSET 0` and `MATERIALIZED` guard trick, `TRY_CONVERT` details, and
the cast-aborts-transaction claim for ordinary casts, none of which the fetched pages state.
Method: documentation only; no commands were run.
