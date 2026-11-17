---
id: computing-software.database-administration.sql.safe-cast-error-handling
name: safe-cast-error-handling
category: computing-software
field: database-administration
product: sql
tags: [sql, safe-cast-error-handling]
level: advanced
status: docs-checked
description: "Convert untrusted text to numbers or dates without aborting the query."
sources: ["https://learn.microsoft.com/en-us/sql/t-sql/functions/try-cast-transact-sql", "https://www.postgresql.org/docs/current/functions-info.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe casts and conversion errors

- SQL Server `TRY_CAST(expr AS type)` returns NULL when the cast fails, but still raises an error if the conversion is explicitly not permitted (for example int to xml). Results depend on format and session settings: `'12/31/2022'` to datetime2 gives NULL under `SET DATEFORMAT dmy`. It does not work on varchar(max) over 8,000 or nvarchar(max) over 4,000.
- PostgreSQL has `pg_input_is_valid(string, type)` returning true or false, and `pg_input_error_info` returning the error details. The manual says they work only for types whose input function reports "soft" errors; otherwise invalid input aborts the transaction as a direct cast would. The page does not give the release that added them, so check your version. Without them, use a guard in CASE or a PL/pgSQL function with an exception handler.
- SQLite CAST never errors on text: it takes the longest numeric prefix, so `CAST('abc' AS INTEGER)` is 0 and `CAST('123e+5' AS INTEGER)` is 123; a NULL input gives NULL. Check the text first if 0 is a legitimate value.
- Guard pattern: `CASE WHEN s ~ '^[0-9]+$' THEN s::int END`. PostgreSQL's CASE does not evaluate subexpressions it does not need, but constant subexpressions can still be evaluated early at planning time, so do not put a failing constant cast inside a CASE arm.
- Self-check: load a dirty column with 'n/a' and blanks and confirm the query completes.

## Checked

Date: 2026-11-08

Method: Read the Microsoft Learn TRY_CAST page, the PostgreSQL manual page functions-info.html (pg_input_is_valid) and the SQLite lang_expr.html CAST section; the draft's "PostgreSQL 16+" and TRY_CONVERT claims are not stated on these pages and were removed.
