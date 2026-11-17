---
id: computing-software.database-administration.query-optimisation.like-and-case-insensitive-search-indexing
name: like-and-case-insensitive-search-indexing
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, composite-index, like-prefix-search, leading-wildcard, case-insensitive-search, text-pattern-ops, collation, function-based-index]
level: practitioner
status: draft
description: "Make LIKE and case-insensitive searches use B-tree indexes: prefix patterns, leading wildcards, collation and operator-class rules, and function-based indexes per engine."
sources:
  - https://use-the-index-luke.com/sql/where-clause/searching-for-ranges/like-performance-tuning
  - https://use-the-index-luke.com/sql/where-clause/functions/case-insensitive-search
  - https://www.postgresql.org/docs/current/indexes-opclass.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LIKE and case-insensitive search

**Goal:** know which text searches a B-tree can serve and what to build for the rest.

## LIKE patterns vs B-tree
| Pattern | Index usable? |
|---|---|
| `LIKE 'abc%'` (prefix) | Yes: becomes a range scan `>= 'abc' AND < 'abd'` |
| `LIKE 'ab%c%'` | Partly: range on `'ab'`, rest filtered |
| `LIKE '%abc'` / `'%abc%'` | No (full index or table scan) |
| `LIKE ?` bind parameter | Depends: some optimisers plan without knowing the pattern |
For leading wildcards use trigram indexes (PostgreSQL pg_trgm), full-text search,
SQL Server full-text, Oracle Text, or store reversed strings for suffix search.

## Engine-specific gotchas for prefix LIKE
- **PostgreSQL**: with a non-C collation, a default B-tree cannot serve LIKE.
  Use `CREATE INDEX ON users (email text_pattern_ops);` (or `COLLATE "C"`).
- **MySQL**: prefix LIKE uses the index; case-insensitivity follows the column
  collation (`_ci` collations are already case-insensitive).
- **SQL Server**: same; default collations are usually CI.
- **SQLite**: LIKE is case-insensitive for ASCII; the index must be `COLLATE NOCASE`
  or set `PRAGMA case_sensitive_like = ON`.

## Case-insensitive equality
`WHERE lower(email) = lower(?)` cannot use a plain index on `email`. Options:
- function-based/expression index on `lower(email)` (PostgreSQL, Oracle; MySQL 8
  functional key parts `INDEX ((lower(email)))`; SQL Server: computed column + index);
- case-insensitive collation on the column (MySQL/SQL Server default `_ci`,
  PostgreSQL nondeterministic ICU collation or `citext`);
- normalise on write (store lowercased email) and search exact.

## Gotchas
- `UPPER()` vs `LOWER()` must match the index expression exactly.
- Unicode case folding (German ß, Turkish i) differs between lower() and collations; pick one consistently.
- Wrapping the column in any function in WHERE (`TRIM`, `CAST`) has the same effect: index unusable unless indexed the same way.

## Verify
EXPLAIN shows an index range scan for the prefix/ci query; with a leading wildcard
confirm the alternative index (trigram/full-text) is used.
