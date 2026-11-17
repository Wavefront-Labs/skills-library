---
id: computing-software.database-administration.sql.dynamic-sql-safe-identifiers
name: dynamic-sql-safe-identifiers
category: computing-software
field: database-administration
product: sql
tags: [sql, dynamic-sql-safe-identifiers]
level: advanced
status: docs-checked
description: "Build dynamic SQL with quoted identifiers and allow-lists, never raw string concatenation."
sources: ["https://www.postgresql.org/docs/current/plpgsql-statements.html", "https://www.postgresql.org/docs/current/functions-string.html", "https://www.postgresql.org/docs/current/functions-matching.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe dynamic SQL for identifiers

- Parameters supply data values, not table or column names: changing a table name means building the command as a string and running it with `EXECUTE`. Use an allow-list in the app, or in PL/pgSQL `EXECUTE format('SELECT %I FROM %I WHERE id = $1', col, tbl) USING id_value`.
- PostgreSQL quoting helpers: `quote_ident()` for identifiers, `quote_literal()` for literals (returns NULL on NULL input), `quote_nullable()` (returns the string `NULL`). In `format()`, `%I` is equivalent to `quote_ident` (error on a NULL value) and `%L` to `quote_nullable`. Prefer `$1` with `USING` for values: no quoting is needed and it is the less injection-prone form.
- Do not rely on dollar-quoting delimiters to protect text that is not known in advance; the page says to use the quote functions.
- Validate sort direction as `ASC|DESC` only.
- LIKE patterns: `%` and `_` are wildcards. Escape them with the escape character (PostgreSQL default is the backslash; `ESCAPE` selects another; in SQLite the optional `ESCAPE` clause takes a single-character string, and that character before `%`, `_` or itself matches the literal).
- Run the app as a low-privilege role.
- Self-check: pass a single quote and `;--` as the identifier or value and confirm the allow-list or quoting rejects or neutralises it instead of running extra SQL.

## Checked

Date: 2026-11-07. Read the PostgreSQL PL/pgSQL "Executing Dynamic Commands" section (plpgsql-statements, the EXECUTE, USING, quote_* and format %I/%L passages; rest of the page searched only), the quote_ident/quote_literal/format entries and the format %I/%L text on String Functions (functions-string, by search), the LIKE escape paragraphs on Pattern Matching (functions-matching, by search), and the ESCAPE paragraph of the SQLite Expressions page (lang_expr, by search). Confirmed the `format('... %I ...') ... USING` form, %I = quote_ident, %L = quote_nullable, quote_literal NULL behaviour, and escape-character rules. Corrected: `%L` was listed beside quote_literal; the page says it matches quote_nullable. The SQLite LIKE line is limited to what its ESCAPE paragraph says; whether SQLite has a default escape character is not stated there, so nothing is claimed. Description changed from "never string concatenation" because the page itself concatenates with quote_ident.
Method: documentation only; no commands were run.
