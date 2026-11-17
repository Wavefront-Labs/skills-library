---
id: computing-software.database-administration.sql.sql-literals-identifiers-and-quoting
name: sql-literals-identifiers-and-quoting
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-lexical-structure, quoted-identifiers, string-literals, sql-comments]
level: intro
status: docs-checked
description: "Write SQL literals, quoted identifiers and comments correctly in PostgreSQL and SQLite, including escaping and case folding."
sources: ["https://www.postgresql.org/docs/current/sql-syntax-lexical.html", "https://www.sqlite.org/lang_keywords.html", "https://www.sqlite.org/quirks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lexical structure

- String literals use single quotes. PostgreSQL: write two single quotes to include one (`'it''s'`). Double quotes delimit identifiers (a delimited identifier is always an identifier, never a keyword); a doubled double quote puts a double quote inside the name. SQLite also accepts square brackets and backticks as non-standard identifier quotes (for SQL Server and MySQL compatibility).
- SQLite quirk: a double-quoted token that matches no identifier is silently treated as a string literal, so a misspelled column name becomes a string and raises no error (SQLite 3.27.0 and later log a warning). Always use single quotes for strings.
- PostgreSQL folds unquoted names to lower case; quoting makes a name case-sensitive (`"Foo"` differs from `foo`). The standard folds to upper case, so for portability either always quote a name or never quote it. Keywords and unquoted identifiers are case-insensitive. Identifiers are truncated to 63 bytes by default.
- Backslash is an ordinary character in a regular PostgreSQL string when `standard_conforming_strings` is on (the default since 9.1). Use an escape string `E'a\nb'` for C-style escapes (`\n`, `\t`, `\xhh`, `\uxxxx`); inside `E'...'` write `\\` for a backslash.
- Typed literals: the `type 'string'` form, for example `DATE '2025-01-31'` or `REAL '1.23'`, or `CAST(...)` / `::` (PostgreSQL). Hex bit strings: `X'1FF'` (PostgreSQL bit-string constant). PostgreSQL dollar quoting (`$$text$$` or `$tag$text$tag$`) writes nothing escaped inside and suits function bodies; tags are case-sensitive and dollar-quoted strings can be nested with different tags.
- Comments: `-- to end of line` and `/* block */`. PostgreSQL block comments nest, as the standard specifies.
- Do not use keywords as names. SQLite recommends never using any English word as a user-defined object name and quoting such names anyway, because new keywords are added over time.
- A semicolon terminates each command; it cannot appear inside a command except in a string constant or quoted identifier.

## Checked

2026-11-08. Confirmed against the PostgreSQL 18 page "Lexical Structure" (identifiers, folding, string constants, escape strings, standard_conforming_strings, dollar quoting, bit strings, typed constants, comments, semicolon), the SQLite keywords page (four quoting forms, advice to quote English words) and the SQLite "Quirks" page (double-quoted string literals, 3.27.0 warning). Removed as unconfirmed: all MySQL claims (backticks as MySQL's own quote, `ANSI_QUOTES`, backslash default, `--` needing a space; the MySQL manual is blocked to fetch), Oracle/SQL Server folding and quoting claims, and the `INTERVAL '1' DAY` example.
Method: documentation only; no commands were run.
