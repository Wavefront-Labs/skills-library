---
id: computing-software.database-administration.sql.find-duplicate-rows
name: find-duplicate-rows
category: computing-software
field: database-administration
product: sql
tags: [sql, find-duplicate-rows]
level: intro
status: docs-checked
description: "Detect duplicates by key with GROUP BY HAVING and window functions."
sources: ["https://www.postgresql.org/docs/current/sql-select.html", "https://www.postgresql.org/docs/current/tutorial-window.html", "https://www.postgresql.org/docs/current/indexes-expressional.html", "https://www.sqlite.org/lang_select.html", "https://www.sqlite.org/windowfunctions.html", "https://www.sqlite.org/expridx.html", "https://www.sqlite.org/lang_corefunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding duplicate rows

- `SELECT email, count(*) FROM users GROUP BY email HAVING count(*) > 1;` (`HAVING` filters groups after aggregation, in both PostgreSQL and SQLite).
- List all rows of duplicates: join back, or use `count(*) OVER (PARTITION BY email)` in a sub-select and filter on it outside: window functions are allowed only in the select list and `ORDER BY` (PostgreSQL) and in the result set and `ORDER BY` (SQLite), so `WHERE`/`HAVING` cannot test them directly.
- Normalise before comparing (`lower(trim(email))`; `lower` and `trim` exist in both engines).
- Prevent recurrence with a unique index on the normalised expression: `CREATE UNIQUE INDEX ... ON users (lower(email))` (PostgreSQL's documented example; SQLite allows expressions in `CREATE INDEX` but not inside `UNIQUE` or `PRIMARY KEY` constraints of `CREATE TABLE`, and only deterministic functions). In SQLite a query uses the index only when its expression is written exactly as in the index.
- Self-check: re-run the detector after cleanup and expect zero rows.

## Checked

Date: 2026-11-07. Read the PostgreSQL Indexes on Expressions page in full, the SQLite Indexes On Expressions page in full, the SQLite Window Functions introduction (section 1, to the row_number example) and the PostgreSQL window tutorial passage on where window functions are allowed (located by search, the surrounding paragraphs read). Searched PostgreSQL SELECT (HAVING clause), SQLite SELECT (HAVING paragraph) and the SQLite core functions list for lower() and trim(). Confirmed: HAVING semantics, window-function placement rules and the sub-select workaround, unique expression index behaviour in PostgreSQL, SQLite expression-index restrictions (exact expression match, deterministic functions only, not in UNIQUE/PRIMARY KEY table constraints). Added those caveats; no claim removed. The list of lower/trim comes from names only on the SQLite function list, not a behavioural reading.
Method: documentation only; no commands were run.
