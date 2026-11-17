---
id: computing-software.database-administration.sql.trim-pad-substring-functions
name: trim-pad-substring-functions
category: computing-software
field: database-administration
product: sql
tags: [sql, trim-pad-substring-functions]
level: intro
status: docs-checked
description: "Use trim, lpad, substr, position and replace for string cleanup."
sources: ["https://www.postgresql.org/docs/current/functions-string.html", "https://www.sqlite.org/lang_corefunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trim pad substring and position functions

PostgreSQL:
- `trim([LEADING | TRAILING | BOTH] [chars] FROM s)` removes the longest run of the listed characters (space by default, BOTH by default). `btrim`, `ltrim` and `rtrim` take an optional character set too.
- `lpad(s, 5, '0')` extends to the length by prepending the fill (space by default); a string longer than the length is truncated on the right.
- `substring(s FROM 2 FOR 3)` and `substr(s, 2, 3)` count from the 1st character. `position('x' IN s)` returns the 1-based index, or 0 if absent.
- `replace(s, 'a', 'b')` replaces all occurrences. `split_part(s, ',', 2)` returns the 2nd field; a negative n counts from the end.
- `length` and `char_length` count characters; `octet_length` counts bytes.
- `concat()` and `concat_ws()` ignore NULL arguments.

SQLite (core functions):
- `trim`, `ltrim`, `rtrim` take an optional second argument listing the characters to remove (space by default).
- There is no `lpad` and no `position(... IN ...)` in the core function list. Use `instr(X, Y)`, which returns the number of prior characters plus 1, or 0 if not found, and NULL if either argument is NULL.
- `substr(X, Y, Z)` starts at the Y-th character, with 1 being the left-most; a negative Y counts from the right. For text the indices count code points, for a BLOB they count bytes. `substring` is an alias from 3.34.
- `replace(X, Y, Z)` uses BINARY comparison and returns X unchanged if Y is empty.
- `length(X)` is the number of characters for text and bytes for a BLOB; `octet_length(X)` is bytes.
- `concat` and `concat_ws` skip NULL arguments (concat_ws returns NULL if the separator is NULL).

Self-check: test empty string, NULL and multibyte input.

## Checked

2026-11-08. Confirmed against the PostgreSQL String Functions and Operators page and the SQLite Core Functions page. Removed the claims that `||` propagates NULL and that SQLite has `lpad`, `position` and `split_part` (not on those pages), and corrected `length` for SQLite (characters for text, bytes only for blobs).

Method: documentation only; no commands were run.
