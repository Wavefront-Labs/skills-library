---
id: computing-software.database-administration.sql.sql-dialect-portability
name: sql-dialect-portability
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-portability, dialect-differences, iso-sql, postgres-vs-mysql, sqlglot]
level: advanced
status: docs-checked
description: "Write portable SQL and know the main dialect differences between PostgreSQL, SQL Server and SQLite, with sqlglot and SQLFluff."
sources: ["https://www.postgresql.org/docs/current/features.html", "https://www.postgresql.org/docs/current/sql-select.html", "https://www.sqlite.org/lang_select.html", "https://learn.microsoft.com/en-us/sql/t-sql/queries/top-transact-sql", "https://www.sqlite.org/lang_upsert.html", "https://www.sqlite.org/datatype3.html", "https://www.sqlite.org/lang_keywords.html", "https://learn.microsoft.com/en-us/sql/t-sql/language-elements/string-concatenation-transact-sql", "https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql", "https://www.postgresql.org/docs/current/functions-string.html", "https://github.com/tobymao/sqlglot/blob/main/README.md", "https://docs.sqlfluff.com/en/stable/gettingstarted.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dialect portability

- The standard is ISO/IEC 9075, revised from time to time; the most recent update is SQL:2023, with SQL:2016 and SQL:2011 before it. Since SQL:1999 it defines a large set of individual features, a subset being the mandatory "Core". The PostgreSQL manual's Appendix D "SQL Conformance" lists what PostgreSQL supports and notes it is not a full statement of conformance. Each engine supports part of the standard with differing syntax and adds extensions.
- Row limiting: PostgreSQL supports `LIMIT` / `OFFSET` and the standard `FETCH FIRST n ROWS ONLY` (with `WITH TIES` needing `ORDER BY`); SQLite has `LIMIT`; SQL Server uses `TOP (n)`, and its manual recommends `OFFSET` / `FETCH` in `ORDER BY` for paging. Always add `ORDER BY` so the rows are predictable.
- String concatenation: `||` in PostgreSQL and SQLite; `+` in SQL Server (a NULL operand yields NULL unless `CONCAT_NULL_YIELDS_NULL` is changed).
- Quoting identifiers: `"x"` in the standard, PostgreSQL and SQLite (SQLite also accepts `[x]`, the quoting used by SQL Server and MS Access, and backticks). PostgreSQL folds unquoted names to lower case where the standard says upper case.
- Booleans: PostgreSQL has a `boolean` type; SQLite has no Boolean storage class (0 and 1 integers); SQL Server's `bit` type is used for Boolean values.
- Upsert: not standard SQL as an `INSERT` clause. SQLite's `INSERT ... ON CONFLICT` follows the syntax established by PostgreSQL, with generalisations.
- Other places dialects diverge: date and time functions, auto-increment syntax, integer division and NULL ordering defaults. Check each against the engine's manual rather than assuming.
- Stay portable by using standard joins, `CASE`, `COALESCE`, `CAST`, `FETCH FIRST`, window functions and CTEs, and keep dialect-specific SQL in a small adapter or query-builder layer. Do not chase full portability if you run one engine.
- Tools: SQLGlot is a Python SQL parser and transpiler that translates between more than 30 dialects (review its output; it aims for, not guarantees, equivalence); SQLFluff is a dialect-aware SQL linter (`sqlfluff lint file.sql --dialect ansi`). Test migrations on the real production engine and version rather than a different engine such as SQLite.

## Checked

2026-11-08. Confirmed against the PostgreSQL 18 pages "SQL Conformance" (standard name, SQL:2023, Core features) and "SELECT" (LIMIT, FETCH FIRST, WITH TIES), the "String Functions" page (`||`), the SQLite pages "SELECT" (LIMIT), "UPSERT", "Datatypes In SQLite" (no Boolean class), "Expressions" (`||`) and "SQLite Keywords" (quoting forms), the Microsoft Learn pages "TOP", "+ (String concatenation)" and "Data types" (`bit` for Boolean values), and the SQLGlot README and SQLFluff getting-started page. Removed as unconfirmed: Oracle claims (empty string equals NULL, boolean before 23ai), MySQL claims, implicit commits on DDL, the Testcontainers recommendation, and per-engine NULL ordering and integer-division claims (see the NULL and numeric skills for PostgreSQL and SQLite).
Method: documentation only; no commands were run.
