---
id: computing-software.database-administration.duckdb.duckdb-columns-expression
name: duckdb-columns-expression
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, columns-expression, unpack, regex, lambda, where, dynamic-sql]
level: advanced
status: docs-checked
description: "Apply one expression to many DuckDB columns with COLUMNS(*), regex or lambda selection, capture-group renaming, WHERE usage and UNPACK into variadic functions."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/expressions/star.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run the same expression across a dynamic set of columns.

`COLUMNS(...)` expands to one expression per matching column. Selectors: `*` (optionally with `EXCLUDE`/`REPLACE`), a regex string, a lambda, or a list of names.

```sql
CREATE TABLE numbers (id INTEGER, number INTEGER);
INSERT INTO numbers VALUES (1, 10), (2, 20), (3, NULL);
SELECT min(COLUMNS(*)), count(COLUMNS(*)) FROM numbers;     -- 4 result columns
SELECT min(COLUMNS(* REPLACE (number + id AS number))), count(COLUMNS(* EXCLUDE (number))) FROM numbers;
SELECT COLUMNS(*) + COLUMNS(*) FROM numbers;                -- combine only if same star expression
SELECT COLUMNS('(id|numbers?)') FROM numbers;               -- regex on column names
SELECT COLUMNS(lambda c: c LIKE '%num%') FROM numbers;      -- lambda predicate
SELECT COLUMNS(['id', 'num']) FROM numbers;                 -- explicit list
```

Pattern operators (`LIKE`, `GLOB`) are not supported inside COLUMNS; use a regex string or lambda instead.

Renaming with capture groups (1-indexed; `\0` is the original name):
```sql
SELECT COLUMNS('(\w{3}).*') AS '\1' FROM numbers;     -- id, num
SELECT COLUMNS('(\w*):(\w*)') AS '\1\2' FROM tbl;     -- "Foo:Bar" -> FooBar
SELECT min(COLUMNS(*)) AS "min_\0" FROM numbers;      -- min_id, min_number
```

In WHERE, conditions apply to every column and are AND-ed:
```sql
SELECT * FROM (...) _(x, y) WHERE COLUMNS(*) = 'a';                 -- x = 'a' AND y = 'a'
SELECT * FROM (...) _(x, y) WHERE greatest(UNPACK(COLUMNS(*) = 'a'));  -- x = 'a' OR y = 'a'
```

UNPACK: without it, a function wrapping COLUMNS is applied per column (`coalesce(COLUMNS(['a','b','c']))` gives 3 columns). With it the columns expand into the parent's arguments: `coalesce(UNPACK(COLUMNS(['a','b','c'])))` gives one column (42 in the docs example). `*COLUMNS(*)` is a shorthand only when applied directly to COLUMNS; `greatest(UNPACK(COLUMNS(*) + 1))` cannot use `*` (syntax error).

## Checked

2026-11-07. Read the Star Expression page in full and confirmed COLUMNS with `*`, REPLACE and EXCLUDE, combining same-star expressions, regex strings, lambda and list forms, no pattern-matching operators inside COLUMNS, capture-group renaming (one-indexed, `\0` original name), WHERE use (AND) and the UNPACK-into-`greatest` OR form, UNPACK versus `*` and its syntax-error warning. Removed the Verify step.

Method: documentation only; no commands were run.
