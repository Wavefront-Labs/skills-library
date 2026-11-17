---
id: computing-software.database-administration.sql.regex-pattern-matching
name: regex-pattern-matching
category: computing-software
field: database-administration
product: sql
tags: [sql, regex-pattern-matching]
level: practitioner
status: docs-checked
description: "Match text with LIKE, ILIKE, POSIX regex operators and SQLite GLOB."
sources: ["https://www.postgresql.org/docs/current/functions-matching.html", "https://www.postgresql.org/docs/current/pgtrgm.html", "https://www.sqlite.org/lang_expr.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LIKE and regular expressions

- `LIKE` matches the whole string: `%` is any run of zero or more characters, `_` exactly one. Put `%` at both ends to match anywhere. The default escape character in PostgreSQL is backslash; change it with `ESCAPE '#'` or disable it with `ESCAPE ''`; double the escape character to match it literally.
- `ILIKE` (PostgreSQL extension) is case-insensitive per the active locale and does not support nondeterministic collations.
- PostgreSQL POSIX regex operators: `~` (match), `~*` (case-insensitive), `!~`, `!~*`. `regexp_replace(s, 'x+', 'y', 'g')` replaces only the first match unless the `g` flag is given. `regexp_matches` returns a set of text arrays (no rows if no match; one row without `g`; N rows with `g`); the manual recommends `regexp_match` when only the first match is wanted.
- SQLite: LIKE is case-insensitive for ASCII by default (`'a' LIKE 'A'` is true; non-ASCII is case-sensitive). `GLOB` uses Unix glob syntax and is case-sensitive. `REGEXP` calls a user function `regexp()` that is not defined by default, so it errors unless the application registers one.
- Indexing: the pg_trgm extension's GIN or GiST trigram indexes support `LIKE`, `ILIKE`, `~` and `~*`, and unlike B-tree searches the pattern need not be left-anchored. A pattern with no extractable trigrams degenerates to a full-index scan.
- Self-check: EXPLAIN a `%foo%` search before and after creating the trigram index and compare the plans.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages functions-matching.html and pgtrgm.html and the SQLite lang_expr.html page; the draft's claims that leading-wildcard patterns cannot use a B-tree index and that GLOB uses `*` and `?` are not stated on those pages, so the first was recast as the pg_trgm comparison and the second dropped.
