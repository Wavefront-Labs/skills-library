---
id: computing-software.database-administration.mongodb.unionwith-combining-collections
name: unionwith-combining-collections
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-aggregation, unionwith, aggregation-pipeline, union-all]
level: practitioner
status: verified
description: "Combine documents from several MongoDB collections in one aggregation with $unionWith, including sub-pipelines, ordering, sharded limits and performance."
sources:
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/unionWith/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $unionWith

**Goal:** report across collections with the same shape (monthly archives, per-region collections, current plus history) without client-side merging. It is SQL `UNION ALL`: duplicates are kept.

## Basic
```javascript
db.sales_2025.aggregate([
  { $project: { _id: 0, store: 1, amount: 1, year: { $literal: 2025 } } },
  { $unionWith: { coll: "sales_2026",
      pipeline: [ { $project: { _id: 0, store: 1, amount: 1, year: { $literal: 2026 } } } ] } },
  { $group: { _id: { store: "$store", year: "$year" }, total: { $sum: "$amount" } } },
  { $sort: { "_id.store": 1, "_id.year": 1 } }
])
```
Shorthand `{ $unionWith: "sales_2026" }` pulls whole documents unchanged.

## Rules worth knowing
- Filter **inside** each sub-pipeline (`$match` first) so each collection uses its own indexes; a `$match` after `$unionWith` cannot use indexes on the second collection.
- Order of output is not guaranteed; add `$sort` after the union.
- Need `UNION` (distinct)? Follow with `$group` on the fields that define a duplicate.
- The sub-pipeline cannot contain `$out` or `$merge` ("$merge is not allowed within a $unionWith's sub-pipeline"); the outer pipeline can end with them (an outer `$merge` wrote all 5 rows into a combined collection).
- Views can be the target `coll`, and `$unionWith` can be used inside a view definition.

## Building a rolling "all years" view
```javascript
db.createView("sales_all", "sales_2025", [ { $unionWith: "sales_2026" } ])
```
Update the view definition (`collMod` with `viewOn`/`pipeline`) when a new yearly collection appears.

## Verify
`explain("executionStats")` shows a `$unionWith` stage with its own nested plan; confirm each branch shows `IXSCAN`, not `COLLSCAN`, when filtered.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. The example (two projections with `$literal` years, `$unionWith` with a sub-pipeline, `$group`, `$sort`) returned the four expected totals (a/2025 5, a/2026 11, b/2025 7, b/2026 2); the shorthand `{ $unionWith: "sales_2026" }` returned all 5 documents.
- `$out`/`$merge` in the sub-pipeline errored; `createView` with `$unionWith` counted 5; `collMod` with `viewOn` and a new pipeline worked; a view as the target `coll` returned 9 documents; explain showed nested plans with `IXSCAN` for a `$match` inside the sub-pipeline on an indexed field. The sharded-collection version claim was not confirmed and was removed.
