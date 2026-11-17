---
id: computing-software.database-administration.mongodb.partial-and-sparse-indexes
name: partial-and-sparse-indexes
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, compound-index, partial-index-mongodb, sparse-index, partialfilterexpression, unique-index]
level: practitioner
status: verified
description: "Use MongoDB partial indexes (partialFilterExpression) instead of sparse indexes to index a subset of documents, enforce conditional uniqueness, and make queries use them."
sources:
  - https://www.mongodb.com/docs/manual/core/index-partial/
  - https://www.mongodb.com/docs/manual/core/index-sparse/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial and sparse indexes

## Partial indexes (preferred)
Index only documents matching a filter: smaller index, cheaper writes for documents outside it.
```js
db.orders.createIndex(
  { customerId: 1, createdAt: -1 },
  { partialFilterExpression: { status: { $in: ["open", "pending"] } } }
)
```
Accepted filter operators on 9.0.4: equality / `$eq`, `$exists: true`, `$gt/$gte/$lt/$lte`, `$type`, `$in`, `$and` and `$or`.
Rejected with "Expression not supported in partial index: $not": `$exists: false`, `$ne`, `$nin`, `$not`; `$regex` is rejected too.

### The query must imply the filter
The planner uses a partial index only if the query predicate is a subset of the filter:
```js
db.orders.find({ customerId: 42, status: "open" })            // uses it
db.orders.find({ customerId: 42 })                             // cannot (might need closed orders)
db.orders.find({ customerId: 42, status: { $in: ["open","pending"] } })   // uses it
```
Make sure the application always includes the filtering condition.

## Conditional uniqueness
```js
// email unique only among active users; deleted users may reuse addresses
// ($exists: false is NOT allowed in a partial filter; equality to null matches missing or null)
db.users.createIndex({ email: 1 },
  { unique: true, partialFilterExpression: { deletedAt: null } })
// unique when present (replacement for unique + sparse)
db.users.createIndex({ externalRef: 1 },
  { unique: true, partialFilterExpression: { externalRef: { $type: "string" } } })
```
Documents outside the filter are not checked for uniqueness at all.

## Sparse indexes (legacy)
`{ sparse: true }` skips documents **missing** the field (but indexes `null` values). Equivalent
to `partialFilterExpression: { field: { $exists: true } }`, which is clearer and more flexible.
Caveat: a sparse index is not used for queries/sorts that must return documents lacking the
field (e.g. `find().sort({ field: 1 })` without a filter), unless hinted, which then silently
omits those documents.

## Gotchas
- You cannot have both `sparse` and `partialFilterExpression` on one index.
- The `_id` index cannot be partial ("not valid for an _id index specification"); the docs say shard key indexes cannot be partial.
- Several partial indexes may share one key pattern if their filters differ (two indexes on `{a: 1}` with filters `{b: 1}` and `{b: 2}` were created on 9.0.4); give each an explicit `name`.
- TTL indexes can be partial: expire only some documents.

## Verify
`db.orders.find({...}).explain("executionStats")` shows IXSCAN on the partial index;
`db.orders.stats().indexSizes` (or `$collStats` with `storageStats`) shows it is much smaller than the full equivalent.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. Partial index on `status` `$in` ["open","pending"]: the query with `status: "open"` and the one with `$in` of the same two values used `IXSCAN`; the query without `status` and the one with `$in: ["open","closed"]` used `COLLSCAN`.
- Filter operators tried one by one: accepted `$eq`, equality, `$exists: true`, `$gt`, `$gte`, `$lt`, `$lte`, `$type`, `$and`, `$or`, `$in`; rejected `$exists: false`, `$ne`, `$nin`, `$not`, `$regex`. The original conditional-uniqueness example with `$exists: false` failed to build; `deletedAt: null` built, rejected a duplicate email among live documents and allowed duplicates among documents with a `deletedAt` date.
- `unique` + `$type: "string"` allowed several documents without the field and rejected a duplicate string (E11000). Sparse index: unfiltered sort used `COLLSCAN` + `SORT`; with `hint` it returned 2 of 3 documents; `find({a: null})` with the hint returned the explicit null. `sparse` with `partialFilterExpression` is rejected ("cannot mix"). TTL with a partial filter built. `indexSizes` listed per index.
- Docs fetched: partial-index page ("Shard key indexes cannot be partial indexes").
