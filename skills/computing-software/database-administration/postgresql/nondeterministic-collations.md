---
id: computing-software.database-administration.postgresql.nondeterministic-collations
name: nondeterministic-collations
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, nondeterministic-collation, icu, case-insensitive, accent-insensitive, citext, collation]
level: practitioner
status: verified
description: "Use ICU nondeterministic collations in PostgreSQL for case- or accent-insensitive equality and unique constraints, and know where they cannot be used."
sources:
  - https://www.postgresql.org/docs/current/collation.html#COLLATION-NONDETERMINISTIC
  - https://www.postgresql.org/docs/current/sql-createcollation.html
  - https://www.postgresql.org/docs/current/citext.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nondeterministic collations for case-insensitive comparison

PG12+ with ICU. A nondeterministic collation compares strings by collation rules rather than bytes, so `'Alice' = 'alice'` can be true and a UNIQUE index enforces it.

## Create
```sql
-- case-insensitive, accent-sensitive
CREATE COLLATION ci (provider = icu, locale = 'und-u-ks-level2', deterministic = false);
-- case- and accent-insensitive
CREATE COLLATION ci_ai (provider = icu, locale = 'und-u-ks-level1', deterministic = false);
```
ICU strength: `level1` base letters only, `level2` + accents, `level3` + case (default, deterministic-like).

## Use
```sql
CREATE TABLE users (email text COLLATE ci UNIQUE);
INSERT INTO users VALUES ('Bob@Example.com');
INSERT INTO users VALUES ('bob@example.com');   -- ERROR: duplicate key
SELECT * FROM users WHERE email = 'BOB@EXAMPLE.COM';  -- finds it, uses the index
SELECT 'Resume' = 'résumé' COLLATE ci_ai;        -- true
```

## Limitations to plan for
- `LIKE`, `ILIKE` and regular expressions on nondeterministic collations raise errors on PG17 (`nondeterministic collations are not supported for LIKE`, `... for ILIKE`, `... for regular expressions`). PG18 release notes allow `LIKE` (and position-search functions); check your version for the rest. Workaround: `col COLLATE "C" LIKE ...` or a separate lower() expression index.
- B-tree deduplication is disabled for such indexes (bigger indexes).
- Slower comparisons than `C`/deterministic collations; not for hot join keys if avoidable.
- Check each operator you rely on: only `=`, ordering and UNIQUE were exercised here; hash partitioning on a nondeterministic-collation key worked on PG17.

## Versus alternatives
| Option | Pros | Cons |
|---|---|---|
| `citext` extension | simple, LIKE works | lowercase-only folding, no accent handling, extension dependency |
| `lower(col)` unique expression index | works everywhere | every query must write `lower()` |
| nondeterministic collation | correct Unicode semantics, index-backed `=` | LIKE limits above |

## Verify
```sql
SELECT collname, collprovider, collisdeterministic, colllocale FROM pg_collation WHERE collname IN ('ci','ci_ai');
```
(`colllocale` is PG17+; older versions use `colliculocale`.)

## Gotchas
- ICU library upgrades can change sort/compare results; indexes on ICU collations need checking after OS upgrades (`pg_collation_actual_version()` vs stored version).
- Changing an existing column's collation rebuilds indexes and can fail on now-duplicate values; dedupe first.

## Checked
- PostgreSQL 17.6 (EDB Windows build with ICU): every statement above ran; the duplicate-key, `=`, accent-insensitive and LIKE/ILIKE/regex error outputs matched; `colllocale` exists on 17 and `colliculocale` does not; `pg_collation_actual_version` returned an ICU version; changing a column's collation then building a unique index failed on the now-equal values. PG17 B-tree docs say text types cannot use deduplication with a nondeterministic collation; PG18 release notes list LIKE support.
