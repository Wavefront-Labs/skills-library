---
id: computing-software.database-administration.sql.sql-injection-and-parameterised-queries
name: sql-injection-and-parameterised-queries
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-injection, parameterised-queries, prepared-statements, query-builders]
level: practitioner
status: docs-checked
description: "Prevent SQL injection with bind parameters, allow-listed identifiers and least-privilege accounts, with PostgreSQL and SQLite specifics."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html", "https://www.psycopg.org/psycopg3/docs/basic/params.html", "https://www.psycopg.org/psycopg3/docs/api/sql.html", "https://www.postgresql.org/docs/current/libpq-exec.html", "https://www.postgresql.org/docs/current/functions-string.html", "https://www.postgresql.org/docs/current/functions-matching.html", "https://www.sqlite.org/lang_expr.html", "https://www.sqlite.org/c3ref/bind_blob.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL injection

- Bind values, never concatenate. psycopg: `cur.execute("SELECT * FROM t WHERE id = %s", (id,))`; query and parameters are sent to the server separately. Never merge values with Python `%` or `+`, never quote the placeholder, and pass a sequence even for one value (`("bar",)`). Placeholder syntax varies by driver: `%s` / `%(name)s` in psycopg, `$1` in PostgreSQL's wire-level API (libpq), `?`, `?NNN` and `:name` in SQLite (bound with `sqlite3_bind_*`).
- Parameter markers stand for data values only, not table or column names or keywords such as `ASC` / `DESC`. Keep structure fixed in code; when the user picks among options, map the choice to a small allow-list of application-owned tokens and reject anything else (map "desc" to the literal `DESC`).
- Dynamic identifiers: use the driver's helper, such as `psycopg.sql.Identifier` composed with `sql.SQL("... {} ...").format(...)`, `PQescapeIdentifier` in libpq, or `format('%I', name)` in PostgreSQL. Quoting an identifier protects the syntax but does not limit which tables the application may reach, so still choose identifiers from a fixed mapping.
- `LIKE` patterns: binding stops injection but not wildcards. In PostgreSQL, `%` and `_` in user input are wildcards; escape them with the escape character (backslash by default, or the `ESCAPE` clause).
- ORMs and query builders: bind untrusted values rather than concatenating them into query strings; the OWASP cheat sheet notes Hibernate queries can be vulnerable.
- Stored procedures are not automatically safe: binding the call's arguments protects the call, not dynamic SQL built inside the procedure. Use static SQL with parameters, or `EXECUTE ... USING` for values in PL/pgSQL and `%I` for identifiers.
- Manual escaping is strongly discouraged as a substitute for binding, because it depends on dialect and configuration.
- Defence in depth: least privilege. Give each application its own database account with only the grants it needs, no DBA or admin rights, no create or delete rights where avoidable, and consider views to expose only needed columns. Least privilege limits damage; it does not prevent injection.
- Review: check code and stored procedures for values concatenated into SQL, and that dynamic identifiers and sort directions come from a fixed mapping.

## Checked

2026-11-08. Confirmed against the OWASP SQL Injection Prevention Cheat Sheet (prepared statements, allow-list mapping, stored procedures, escaping discouraged, least privilege, views), the psycopg 3 "Passing parameters" and "sql module" pages (`%s`, separate sending, `sql.Identifier`), the PostgreSQL 18 pages "Command Execution Functions" (`$1`, `PQescapeIdentifier`), "String Functions" (`format` with `%I` and `%L`), "Pattern Matching" (LIKE escape), and the SQLite "Expressions" (`?NNN`, `:AAAA` parameters) and `sqlite3_bind_*` pages. Removed as unconfirmed: "parameters cannot stand in for `LIMIT` in every driver", array-parameter `= ANY($1)` list expansion, "no stacked-statement drivers", hiding error messages, WAF as a backstop, and sqlmap testing.
Method: documentation only; no commands were run.
