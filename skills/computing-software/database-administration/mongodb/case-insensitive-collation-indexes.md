---
id: computing-software.database-administration.mongodb.case-insensitive-collation-indexes
name: case-insensitive-collation-indexes
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, collation-index, case-insensitive, mongodb-collation, mongodb-indexes]
level: practitioner
status: verified
description: "Make MongoDB queries case- and accent-insensitive using collation-specific indexes (strength 1 or 2) instead of slow regex, and match query collation to the index."
sources:
  - https://www.mongodb.com/docs/manual/core/index-case-insensitive/
  - https://www.mongodb.com/docs/manual/reference/collation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Case-insensitive indexes with collation

**Goal:** `find({username: "Alice"})` should match `alice`, using an index. `/^alice$/i` regex cannot use an index efficiently (case-insensitive regex scans the whole index).

## Create
```javascript
db.users.createIndex({ username: 1 }, { collation: { locale: "en", strength: 2 } })
```
| strength | Ignores |
|---|---|
| 1 | case and diacritics (`é` = `e` = `E`) |
| 2 | case only |
| 3 (default) | nothing (binary-ish comparison of case) |

## Query must name the same collation
```javascript
db.users.find({ username: "ALICE" }).collation({ locale: "en", strength: 2 })
```
Without `.collation(...)` (or with a different locale/strength) the planner will not use that index and does a case-sensitive match.

## Easier: collection default collation
```javascript
db.createCollection("users", { collation: { locale: "en", strength: 2 } })
```
Every index and query on the collection inherits it unless overridden. Cannot be changed later without copying to a new collection (`collMod` rejects a `collation` field on 9.0.4).

## Gotchas
- Collation affects sort order and string comparison operators (`$lt` on strings) as well as equality.
- Unique + collation index enforces case-insensitive uniqueness (good for usernames).
- `$regex` ignores collation: `find({username: /ALICE/}).collation({locale:"en", strength:2})` matched 0 documents for `alice` on 9.0.4. Test `$text` and `$lookup` yourself before relying on them.
- `locale: "simple"` means binary comparison and is what you get without collation.
- Numeric ordering: `numericOrdering: true` sorts `"10"` after `"9"`.

## Verify
`db.users.find({username:"ALICE"}).collation({locale:"en",strength:2}).explain()` shows `IXSCAN` on `username_1` and `indexBounds` over collation keys.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. Index with `{locale:"en", strength:2}`: `find({username:"ALICE"}).collation(...)` matched `alice` with `IXSCAN` and `CollationKey` index bounds; the same query without `.collation` matched 0 and used `COLLSCAN`.
- Strength on `e`, `é`, `E`: strength 1 matched 3, strength 2 matched 2, strength 3 matched 1. A collection-default collation with a unique index rejected `AL` after `Al` (E11000 naming the collation). `numericOrdering: true` sorted `"9"` before `"10"`.
- Docs fetched: collation reference and case-insensitive index pages (both sources load).
