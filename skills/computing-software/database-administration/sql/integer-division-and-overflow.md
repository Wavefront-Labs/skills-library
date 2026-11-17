---
id: computing-software.database-administration.sql.integer-division-and-overflow
name: integer-division-and-overflow
category: computing-software
field: database-administration
product: sql
tags: [sql, integer-division-and-overflow]
level: practitioner
status: docs-checked
description: "Handle integer division truncation and overflow in PostgreSQL and SQLite."
sources: ["https://www.postgresql.org/docs/current/functions-math.html", "https://www.postgresql.org/docs/current/datatype-numeric.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integer division and overflow

- PostgreSQL: division of integral types truncates toward zero (`5 / 2` is 2, `(-5) / 2` is -2, `5.0 / 2` is 2.5000000000000000). SQLite: an integer divide yields an integer truncated toward zero. To get a fraction, make one operand non-integral (`7/2.0`).
- Overflow, PostgreSQL: `smallint` spans -32768 to +32767, `integer` -2147483648 to +2147483647 (about 2.1 billion), `bigint` +/-9223372036854775807; storing a value outside the range gives an error. Use `bigint` when `integer` may be insufficient (counters, ids).
- Overflow, SQLite: arithmetic stays integer only if both operands are integers and no overflow would result; otherwise it switches to floating point (IEEE 754). An integer literal outside the signed 64-bit range is a floating point literal.
- SQLite `%` casts both operands to INTEGER first, then takes the remainder; PostgreSQL `%` exists for smallint, integer, bigint and numeric (`5 % 4` is 1), and `div(y, x)` gives the numeric integer quotient truncated toward zero.
- Self-check: run `SELECT 7/2, -7/2, 7%3, -7%3` in your engine and compare with the rule above.

## Checked

Date: 2026-11-07. Read the PostgreSQL arithmetic operator table and div/mod rows (functions-math), the integer type table and integer text (datatype-numeric) and the SQLite operator paragraph and numeric literal paragraph (lang_expr). Removed: SQL Server and MySQL claims (no page read), the exact PostgreSQL message text `integer out of range` (the page says only "an error"), and "`%` follows the dividend sign" (no page states it). Corrected: SQLite does not "promote silently"; the page says integer arithmetic is replaced by floating point when it would overflow.
Method: documentation only; no commands were run.
