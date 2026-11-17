---
id: computing-software.database-administration.sql.string-concat-and-quoting-dialects
name: string-concat-and-quoting-dialects
category: computing-software
field: database-administration
product: sql
tags: [sql, string-concat-and-quoting-dialects]
level: intro
status: docs-checked
description: "Handle identifier quoting, concatenation and common function name differences."
sources: ["https://www.postgresql.org/docs/current/sql-syntax-lexical.html", "https://www.postgresql.org/docs/current/functions-string.html", "https://www.postgresql.org/docs/current/functions-conditional.html", "https://learn.microsoft.com/en-us/sql/t-sql/language-elements/string-concatenation-transact-sql"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concatenation quoting and function differences

- PostgreSQL identifiers: unquoted names and key words are case-insensitive; a double-quoted identifier can contain any character except code zero, and a double quote inside is written as two. Quote only when needed.
- PostgreSQL concatenation: `||` accepts non-string input if at least one side is a string (`'Value: ' || 42`); `concat(a, b, ...)` ignores NULL arguments; `concat_ws(sep, ...)` joins with a separator and also skips NULLs.
- T-SQL concatenation: the `+` operator. A NULL operand normally gives NULL, depending on the session setting `CONCAT_NULL_YIELDS_NULL`. A zero-length string is not NULL and concatenates normally.
- Use the standard `COALESCE(a, b, ...)` (returns its first non-null argument) instead of vendor functions such as `IFNULL`, `ISNULL` or `NVL`.
- Self-check: list dialect-specific tokens (`||` vs `+`, quoting characters, vendor null functions) in the code base before a migration, and run the query on the target engine.

## Checked

2026-11-08. Confirmed against the PostgreSQL lexical structure, string function and conditional expression pages, and the T-SQL string concatenation page. Removed the MySQL backtick, SQL Server bracket and MySQL/SQL Server `CONCAT()` claims, the boolean-type differences across PostgreSQL, SQLite and MySQL, and the Oracle `||` claim, because no readable page for them was fetched.
Method: documentation only; no commands were run.
