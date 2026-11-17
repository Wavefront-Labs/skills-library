---
id: computing-software.database-administration.mongodb.aggregation-pipeline-optimization-and-allowdiskuse
name: aggregation-pipeline-optimization-and-allowdiskuse
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, aggregation-pipeline, aggregation-optimization, allowdiskuse, explain, slot-based-execution, pipeline-coalescence, match-early, memory-limit]
level: practitioner
status: verified
description: "Make MongoDB aggregations fast: stage order for index use, what the optimizer reorders, $group/$sort memory limits, allowDiskUse, and reading explain output."
sources:
  - https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/
  - https://www.mongodb.com/docs/manual/core/aggregation-pipeline-limits/
  - https://www.mongodb.com/docs/manual/reference/method/db.collection.aggregate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aggregation pipeline optimization and allowDiskUse

**Goal:** pipelines that use indexes, stay inside memory limits, and do not scan the collection by accident.

## Index use happens only at the start
Indexes serve the leading stages: an initial `$match`, `$sort` and `$limit`, a `$geoNear` (must be the first stage) and, for `$sort` followed by `$group` with `$first`, a `DISTINCT_SCAN`. Anything after `$group`, `$unwind` or a `$project` that computes fields runs on the stream.
```javascript
[ { $match: { tenant: 7, createdAt: { $gte: d } } },  // IXSCAN on {tenant:1, createdAt:1}
  { $sort: { createdAt: -1 } },                         // same index, no in-memory sort
  { $limit: 100 }, ... ]
```

## What the optimizer does for you
- Moves `$match` ahead of `$project`/`$addFields`/`$set` when it does not depend on computed fields.
- Coalesces `$sort` + `$limit` into a top-k sort; `$limit` + `$limit`; `$match` + `$match`.
- `$lookup` + `$unwind` of the same field merges.
- Projection pushdown: only needed fields are fetched (do not add `$project` just for speed; it can block optimizations).
- On 9.0.4 eligible `$group`, `$sort` and `$lookup` run in the slot-based engine; `explain` shows `queryPlanner.winningPlan.queryPlan` with `slotBasedPlan`.

## Memory
- Blocking stages (`$group`, `$sort`, `$bucket`, `$setWindowFields`, `$facet` sub-pipelines) are limited to 100 MB each.
- Over the limit without opting in, a `$sort` fails with "Sort exceeded memory limit of 1048576 bytes, but did not opt in to external sorting" (tested with the limit lowered to 1 MB and `allowDiskUse: false`).
- `allowDiskUse: true` lets them spill (explain showed `usedDisk: true`, `spills: 4`); the dbPath has a `_tmp` folder. `getParameter allowDiskUseByDefault` returned true on 9.0.4, so omitting the option also allows spilling.
```javascript
db.events.aggregate(pipeline, { allowDiskUse: true, maxTimeMS: 60000, comment: "daily-rollup" })
```
Spilling works but is slow; first reduce documents with `$match` and fields with an early `$project` of just what `$group` needs.

## Explain
```javascript
db.events.explain("executionStats").aggregate(pipeline)
```
Look for `COLLSCAN` in the `$cursor` stage, `totalDocsExamined` vs `nReturned`, `usedDisk: true`, and per-stage `executionTimeMillisEstimate`.

## Gotchas
- `$unwind` early multiplies documents; filter arrays with `$filter` instead when possible.
- The `comment` you set appears as `command.comment` in `system.profile` (tested), which helps find a pipeline in the profiler.
- For sharded collections read the sharded aggregation docs; no sharded cluster was run here.

## Verify
After adding the index and reordering, `explain` shows IXSCAN, docsExamined close to nReturned, and no `usedDisk`.

## Checked
- MongoDB 9.0.4 Community, mongosh 2.13.0 and Database Tools 100.19.1 (mongostat, mongotop) on Windows, run in a scratch folder. 30,000-document collection. `$match` + `$sort` + `$limit` with `{k: 1, _id: -1}` gave `LIMIT` > `FETCH` > `IXSCAN` with no `SORT`; `$match` + `$project` of an indexed field gave `PROJECTION_COVERED`. `allowDiskUse`, `maxTimeMS` and `comment` options were accepted, and the comment landed in `system.profile`.
- With `internalQueryMaxBlockingSortMemoryUsageBytes` lowered to 1 MB: `allowDiskUse: false` raised the quoted error; `allowDiskUse: true` reported `usedDisk: true`, `spills: 4`, `spilledDataStorageSize` 186781. The optimizer behaviours listed are the ones seen in the explaining-aggregation-pipelines skill (`$match` before `$project`, merged `$match`, `$sort`+`$limit`).
- Not asserted after review: `$group` error wording, shard merge behaviour (no sharded cluster), and the `$search` index claim (Atlas only).
