---
id: computing-software.database-administration.sql.sql-numeric-types-and-decimal-precision
name: sql-numeric-types-and-decimal-precision
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-data-types, numeric-decimal, float-vs-decimal, integer-overflow, money]
level: practitioner
status: docs-checked
description: "Choose integer, NUMERIC and floating types in PostgreSQL and SQLite, and handle rounding, overflow, division and ids."
sources: ["https://www.postgresql.org/docs/current/datatype-numeric.html", "https://www.postgresql.org/docs/current/functions-math.html", "https://www.sqlite.org/datatype3.html", "https://www.sqlite.org/stricttables.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric types

- PostgreSQL integers: `smallint` (2 bytes, -32768 to 32767), `integer` (4 bytes), `bigint` (8 bytes, up to 9223372036854775807). Storing a value outside the range raises an error. `integer` is the usual choice; use `bigint` when its range may be insufficient, such as ids that can pass 2147483647.
- Exact: `numeric(p,s)` / `decimal`, user-specified precision, up to 131072 digits before and 16383 after the decimal point when unconstrained; the maximum explicit precision is 1000. The manual recommends `numeric` for monetary amounts, and notes it is slow compared with integer and floating types. Approximate: `real` (4 bytes, 6 decimal digits) and `double precision` (8 bytes, 15 digits), IEEE 754, so some values are stored as approximations. Never store money in floating types; use `numeric` or integer minor units.
- Do not compare floats with `=` for exactness: stored values may differ slightly from what was written.
- Integer division truncates toward zero in PostgreSQL (`5 / 2` is `2`, `5.0 / 2` is `2.5000000000000000`) and in SQLite (integer divide yields an integer). Cast an operand to get fractional results: `5::numeric / 2` or `CAST(5 AS REAL) / 2` in SQLite.
- Rounding ties: PostgreSQL `numeric` rounds ties away from zero, while `real` / `double precision` round ties to the nearest even number on most machines.
- PostgreSQL `NaN` sorts as equal to itself and greater than all non-NaN values, unlike IEEE 754 comparison.
- Auto-increment: SQL-standard identity columns (`GENERATED ... AS IDENTITY`) or the PostgreSQL notational types `serial` / `bigserial`, implemented with sequences, so gaps appear (for example after a rollback). `bigserial` is for when you expect more than 2^31 identifiers.
- SQLite uses type affinity (column affinity is one of BLOB, TEXT, INTEGER, REAL, NUMERIC), so a declared type does not by itself stop a wrong-typed value. Adding the `STRICT` table option enforces the column types (allowed names include `ANY` for untyped columns); a value that cannot be losslessly converted raises an error. SQLite does integer arithmetic when both operands are integers and no overflow would result, otherwise IEEE 754 floating point.

## Checked

2026-11-08. Confirmed against the PostgreSQL 18 pages "Numeric Types" (ranges, numeric limits, money recommendation, float inexactness, rounding ties, NaN ordering, serial and gaps) and "Mathematical Functions and Operators" (integer division truncates toward zero), and the SQLite pages "Datatypes In SQLite" (type affinity), "STRICT Tables" and "Expressions" (integer arithmetic, integer divide truncated toward zero). Removed as unconfirmed: all MySQL and SQL Server claims (MySQL `5/2`, `DIV`, non-strict clamping, `AUTO_INCREMENT`), `NUMERIC(19,4)` as a recommended size, "numeric division yields extra scale", and the SQLite `AUTOINCREMENT`/rowid note.
Method: documentation only; no commands were run.
