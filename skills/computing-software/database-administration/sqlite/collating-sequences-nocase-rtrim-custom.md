---
id: computing-software.database-administration.sqlite.collating-sequences-nocase-rtrim-custom
name: collating-sequences-nocase-rtrim-custom
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, nocase, collation, rtrim, sqlite-schema, case-insensitive]
level: practitioner
status: gated
description: "Use SQLite collating sequences BINARY, NOCASE and RTRIM on columns, indexes and queries, know NOCASE's ASCII-only limit, and register custom collations."
sources:
  - https://sqlite.org/datatype3.html#collation
  - https://sqlite.org/c3ref/create_collation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collating sequences (NOCASE / RTRIM / custom)

## Built-ins
| Collation | Behaviour |
|---|---|
| BINARY (default) | memcmp() byte comparison |
| NOCASE | folds ASCII A-Z to a-z only |
| RTRIM | ignores trailing spaces |

## Where collation comes from
```sql
CREATE TABLE users (email TEXT COLLATE NOCASE UNIQUE, code TEXT);
SELECT * FROM users WHERE email = 'Ann@Example.com';              -- uses column collation
SELECT * FROM users WHERE code = 'ab' COLLATE NOCASE;             -- explicit
CREATE INDEX idx_users_code_nc ON users(code COLLATE NOCASE);     -- index for that query
SELECT * FROM users ORDER BY email COLLATE BINARY;
```
Precedence (datatype3 docs): an explicit `COLLATE` on either operand (left wins) > a column operand's declared collation (left wins) > BINARY. An expression such as `d || ''` has no collation, so BINARY applies.

An index is usable only when its collation matches the comparison's collation: tested on 3.50.4, with only a BINARY index `WHERE code = ? COLLATE NOCASE` gave `SCAN`, and after adding the NOCASE index `SEARCH ... USING INDEX`.

## The Unicode gap
NOCASE does not fold `É`/`é` or `Ü`/`ü`. Options:
- Store a normalised copy (folded in the app) in a generated column and index that.
- Build SQLite with the ICU extension and load a locale collation (gated: unconfirmed, source is paywalled or blocked).
- Register a custom collation from the app.

## Custom collations
```python
con.create_collation("natsort", lambda a, b: (natural_key(a) > natural_key(b)) - (natural_key(a) < natural_key(b)))
con.execute("SELECT name FROM files ORDER BY name COLLATE natsort")
```
`natural` is a reserved word (join keyword), so `COLLATE natural` is a syntax error; pick another name. Every connection that writes to or sorts with an index using that collation must register it, or statements fail with `no such collation sequence: natsort` (reproduced on 3.50.4; plain reads that use the index still worked). Tools like the sqlite3 shell will not be able to use such indexes.

## Gotchas
- `LIKE` is case-insensitive for ASCII by default (`'ABC' LIKE 'abc'` is 1, `'É' LIKE 'é'` is 0 on 3.50.4).
- UNIQUE with NOCASE prevents `Ann@x` and `ann@x` coexisting: decide deliberately.

## Verify
`EXPLAIN QUERY PLAN` for the case-insensitive query shows `USING INDEX` with the NOCASE index.
