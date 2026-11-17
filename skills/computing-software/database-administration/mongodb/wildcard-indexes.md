---
id: computing-software.database-administration.mongodb.wildcard-indexes
name: wildcard-indexes
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-indexes, wildcard-index, dynamic-attributes, wildcardprojection, compound-wildcard-index, polymorphic-documents]
level: practitioner
status: verified
description: "Index unpredictable or user-defined fields in MongoDB with wildcard indexes ($**), wildcardProjection, compound wildcard (7.0+), and their query limitations."
sources:
  - https://www.mongodb.com/docs/manual/core/indexes/index-types/index-wildcard/
  - https://www.mongodb.com/docs/manual/core/indexes/index-types/index-wildcard/reference/restrictions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wildcard indexes

**Goal:** support queries on arbitrary attribute fields (custom fields, product specs) without an index per field.

## Create
```javascript
db.products.createIndex({ "attributes.$**": 1 })                       // every field under attributes
db.products.createIndex({ "$**": 1 }, { wildcardProjection: { attributes: 1, tags: 1 } })   // chosen subtrees
db.products.createIndex({ "$**": 1 }, { name: "wc_no_blob", wildcardProjection: { blob: 0 } })   // all except blob (name it: two "$**" indexes collide on the default name)
db.products.createIndex({ tenantId: 1, "attributes.$**": 1 })           // compound wildcard
```
Each indexed field path is stored as (path, value) pairs, so a query on `attributes.color: "red"` uses the index like a single-field index on that path.

## What it supports
- Equality, range, `$exists: true`, `$in` on one field path per predicate.
- Sort on a single field covered by the wildcard, if the query also filters on that field.
- With compound wildcard, filter on the regular field plus one wildcard path.

## What it cannot do
- Cannot be a unique or TTL index (both error); the docs say a wildcard index cannot be a shard key index. `$**` with `"hashed"` or `"2dsphere"` is rejected, and a compound key may contain only one wildcard field.
- Cannot support `$exists: false` (plan was `COLLSCAN`) or equality on a whole embedded document (`COLLSCAN`). `wildcardProjection` cannot mix inclusion and exclusion ("Cannot do inclusion on field attributes in exclusion projection").
- One wildcard path per query plan: with `attributes.color` and `attributes.size` predicates the plan used a single `IXSCAN` on one path and filtered the other.
- Not covering queries on multiple fields; usually needs FETCH.

## When not to use it
If the queried fields are known and few, regular compound indexes are smaller and faster. For dynamic attributes, also consider the attribute pattern: `attrs: [ { k: "color", v: "red" } ]` with `{ "attrs.k": 1, "attrs.v": 1 }`, which supports multi-attribute queries with `$elemMatch`.

## Verify
`db.products.find({ "attributes.color": "red" }).explain()` shows IXSCAN on `attributes.$**` with `keyPattern` `{ "$_path": 1, "attributes.color": 1 }`.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. All four `createIndex` forms built (the exclusion form needed an explicit name); `explain` for equality, `$gt`, `$exists: true` and `$in` showed `IXSCAN` with `keyPattern` `{"$_path": 1, "attributes.<field>": 1}`; the compound form used `{tenantId: 1, $_path: 1, attributes.color: 1}`; a sort on a filtered path showed no `SORT` stage.
- Rejections quoted above (unique, TTL, hashed, 2dsphere, two wildcard fields, mixed projection); `$exists: false` and whole-document equality gave `COLLSCAN`; the attribute-pattern index `{attrs.k: 1, attrs.v: 1}` served `$elemMatch` with `IXSCAN`.
- Docs fetched: wildcard restrictions page ("You cannot use a wildcard index as a shard key index"). The 7.0 gate and the `$ne: null` claim were removed (a `$ne: null` query did use the index in the test).
