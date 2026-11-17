---
id: computing-software.database-administration.sqlite.like-and-glob-optimization
name: like-and-glob-optimization
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, like-optimization, glob, case-sensitive-like, sqlite-query-planner, prefix-search]
level: practitioner
status: verified
description: "Make SQLite LIKE and GLOB prefix searches use indexes: the exact collation, affinity and pragma conditions, plus FTS5 for infix search."
sources:
  - https://sqlite.org/optoverview.html#the_like_optimization
  - https://sqlite.org/pragma.html#pragma_case_sensitive_like
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LIKE / GLOB optimization

**Goal:** `WHERE name LIKE 'smi%'` as an index range scan instead of a full table scan.

## Conditions for LIKE to use an index (all required)
1. The pattern is a string literal, or a parameter bound to a string, that does **not** begin with a wildcard (statements prepared with `sqlite3_prepare_v2()`/`16_v2` are recompiled on the first step after the binding changes).
2. Either the left side is an indexed column with TEXT affinity, or the pattern does not begin with `-` or a digit (numbers do not sort lexicographically).
3. LIKE/GLOB have not been overloaded with `sqlite3_create_function()`.
4. Case rules match the index collation:
   - default LIKE is case-insensitive (ASCII) → the index must use `COLLATE NOCASE`;
   - with `PRAGMA case_sensitive_like = ON` → index must use BINARY (default).
5. If an `ESCAPE` clause is used, the escape character must be ASCII (or a single-byte UTF-8 character). GLOB needs a BINARY-collated index.

```sql
CREATE INDEX idx_people_name_nc ON people(name COLLATE NOCASE);
EXPLAIN QUERY PLAN SELECT * FROM people WHERE name LIKE 'smi%';
-- SEARCH people USING INDEX idx_people_name_nc (name>? AND name<?)
```
SQLite rewrites it as `name >= 'smi' AND name < 'smj'` plus the original LIKE check.

## GLOB
Always case-sensitive; uses a BINARY-collated index:
```sql
CREATE INDEX idx_files_path ON files(path);
SELECT * FROM files WHERE path GLOB '/var/log/*';
```

## case_sensitive_like caveat
The pragma is a connection-level mode that changes LIKE semantics everywhere on that connection; prefer GLOB for case-sensitive prefix searches (`'a' GLOB 'A'` is 0 on 3.50.4, `'a' LIKE 'A'` is 1).

## Infix and suffix searches
`LIKE '%smith%'` always scans. Options:
- FTS5 with the `trigram` tokenizer supports indexed substring LIKE/GLOB (not with `remove_diacritics`; with `case_sensitive=1` only GLOB; not with an ESCAPE clause; patterns need a run of non-wildcard characters or it scans). Reproduced: `LIKE '%mit%'` found `hello smith`.
- Store a reversed copy in a generated column and index it for suffix search.

## Verify
`EXPLAIN QUERY PLAN` shows `SEARCH ... (name>? AND name<?)`; if it shows `SCAN`, check collation and column affinity first.
