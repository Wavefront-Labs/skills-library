---
id: computing-software.database-administration.mongodb.aggregation-lookup-and-unwind
name: aggregation-lookup-and-unwind
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, aggregation-pipeline, aggregation-lookup, lookup-stage, unwind, join, pipeline-lookup, foreign-field-index, mongosh]
level: practitioner
status: verified
description: "Join MongoDB collections with $lookup (equality and pipeline forms) and $unwind, index the foreign field, and avoid result-size and sharding pitfalls."
sources:
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $lookup and $unwind

**Goal:** the occasional join in MongoDB runs on an index and produces documents
of sane size.

## Equality lookup
```javascript
db.orders.aggregate([
  { $match: { status: "open", createdAt: { $gte: ISODate("2026-10-01") } } },   // filter FIRST
  { $lookup: { from: "customers", localField: "customerId", foreignField: "_id", as: "customer" } },
  { $unwind: "$customer" },                                    // array of 1 -> embedded doc
  { $project: { _id: 1, total: 1, "customer.name": 1, "customer.tier": 1 } }
])
```
`foreignField` should be indexed in the `from` collection. With an index, explain shows
`strategy: "IndexedLoopJoin"` and `indexesUsed` for the lookup; with no index on a small
`from` collection it showed `strategy: "HashJoin"`, otherwise expect a collection scan per input document.

## Pipeline form (filters, projections inside the join)
```javascript
{ $lookup: {
    from: "payments",
    localField: "_id", foreignField: "orderId",          // 5.0+: combine with pipeline
    pipeline: [ { $match: { state: "settled" } }, { $project: { amount: 1, _id: 0 } } ],
    as: "payments" } }
```
`let` + `$expr` in an inner `$match` is the form for non-equality or computed conditions. In explain on 9.0.4 an `$expr` `$eq` on `_id` showed `COLLSCAN` and no `IXSCAN`, so use `localField`/`foreignField` for plain equality.

## $unwind options
```javascript
{ $unwind: { path: "$items", preserveNullAndEmptyArrays: true, includeArrayIndex: "pos" } }
```
Without `preserveNullAndEmptyArrays`, documents with empty/missing arrays
disappear: an inner join by accident.

## Gotchas
- The joined array lives inside one output document: big one-to-many lookups hit
  the 16 MB document limit (`$lookup` with `$unwind` right after is coalesced by
  the optimizer: explain shows one `$lookup` stage with an `unwinding` field).
- `from` collection sharded: supported from 5.1; earlier it had to be unsharded.
- If you need the join on every read, the schema probably wants embedding or the
  extended-reference pattern instead.

## Verify
```javascript
db.orders.explain("executionStats").aggregate([...])
```
The `$lookup` stage shows `indexesUsed` on the foreign field and
`totalDocsExamined` close to the number returned.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. Equality `$lookup` + `$unwind` + `$project`, the `localField`/`foreignField` + `pipeline` form, and `$unwind` with `preserveNullAndEmptyArrays` and `includeArrayIndex` all ran; `$unwind` on a missing field returned 0 documents.
- explain on a 300-document collection: `IndexedLoopJoin` with `indexesUsed` for indexed foreign fields, `HashJoin` for an unindexed one, and the `$lookup`+`$unwind` pair coalesced into one stage with `unwinding`.
- Docs fetched: `$lookup` (sharded `from` supported "Starting in MongoDB 5.1"; the localField + pipeline form is marked New in 5.0).
