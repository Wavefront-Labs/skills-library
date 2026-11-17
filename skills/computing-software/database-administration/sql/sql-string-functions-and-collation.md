---
id: computing-software.database-administration.sql.sql-string-functions-and-collation
name: sql-string-functions-and-collation
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-strings, collation, like-wildcards, string-concatenation, case-sensitivity]
level: practitioner
status: docs-checked
description: "Manipulate text in PostgreSQL and SQLite: concatenation and NULL, LIKE escaping, pattern matching and collations."
sources: ["https://www.postgresql.org/docs/current/functions-string.html", "https://www.postgresql.org/docs/current/functions-matching.html", "https://www.postgresql.org/docs/current/collation.html", "https://www.sqlite.org/datatype3.html", "https://www.sqlite.org/lang_corefunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strings and collation

- Concatenation: PostgreSQL has `||` (a non-string operand is converted to text) and `concat()`/`concat_ws()`, which ignore NULL arguments. SQLite has `concat()` (concatenates the non-NULL arguments, and returns an empty string if all are NULL) and `concat_ws(SEP, ...)` (NULL if the separator is NULL). Be explicit about NULLs with `COALESCE` when mixing engines.
- Length: PostgreSQL `char_length` counts characters and `octet_length` counts bytes. SQLite `length` counts code points for text and bytes for a BLOB; `octet_length` counts bytes.
- Standard-style functions in PostgreSQL: `substring(s FROM 2 FOR 3)`, `position(sub IN s)`, `trim`, `upper`/`lower`. SQLite uses `substr` and `instr`. See `computing-software.database-administration.sql.trim-pad-substring-functions`.
- `LIKE` uses `%` (any string) and `_` (any one character). To match them literally put the escape character before them: in PostgreSQL the default is backslash and `ESCAPE` picks another or `ESCAPE ''` disables it; the SQL standard has no default escape. `ILIKE` (case-insensitive by locale) is a PostgreSQL extension. SQLite supports `LIKE ... ESCAPE` and `GLOB`.
- PostgreSQL regular expressions: `~` is a case-sensitive POSIX match; `SIMILAR TO` uses the SQL-standard regex notation and must match the whole string, like LIKE. SIMILAR TO and POSIX regexes do not support nondeterministic collations.
- Collation decides comparison and sort. PostgreSQL: the `C` and `POSIX` collations sort by byte value and only treat ASCII A to Z as letters; the default collation is the locale chosen at database creation. A nondeterministic ICU collation (`deterministic = false`) can ignore case and accents.- SQLite: the default is BINARY (memcmp). NOCASE folds only the 26 ASCII upper-case letters; RTRIM ignores trailing spaces. A column's collation is set with COLLATE in its definition, and an explicit COLLATE on the left operand wins in a comparison.
- Self-check: compare `'a' = 'A'` under the default and a case-insensitive collation, and an `ESCAPE` pattern against a value that contains a literal `%`.

## Checked

2026-11-08. Confirmed against PostgreSQL String Functions, Pattern Matching and Collation Support pages, and the SQLite Datatypes and Core Functions pages. Removed claims these pages do not cover: MySQL and SQL Server concatenation, default collations and `utf8mb4`, MySQL PAD SPACE trailing-space handling, the "leading wildcard defeats a B-tree index" rule, the requirement that index and query collations match, and the ISO root source.

Method: documentation only; no commands were run.
