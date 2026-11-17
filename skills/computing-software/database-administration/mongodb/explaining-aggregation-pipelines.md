---
id: computing-software.database-administration.mongodb.explaining-aggregation-pipelines
name: explaining-aggregation-pipelines
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, aggregation-explain, mongodb-explain, aggregation-pipeline, query-planning]
level: practitioner
status: verified
description: "Read explain output for MongoDB aggregation pipelines to see which stages use indexes, what gets pushed into the query layer or SBE, and where time and memory go."
sources:
  - https://www.mongodb.com/docs/manual/reference/method/db.collection.explain/
  - https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/
  - https://www.mongodb.com/docs/manual/reference/explain-results/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Explaining aggregation pipelines

**Goal:** know why a pipeline is slow: collection scan at the start, a blocking `$group`/`$sort` spilling, or a `$lookup` doing a scan per document.

## Run it
```javascript
db.orders.explain("executionStats").aggregate([
  { $match: { status: "paid", createdAt: { $gte: ISODate("2026-10-01") } } },
  { $sort: { createdAt: -1 } },
  { $group: { _id: "$customerId", n: { $sum: 1 } } }
])
```
Verbosity: `queryPlanner` (plan only), `executionStats` (runs it), `allPlansExecution`.

## Read it
- **`stages[0].$cursor`** or **`queryPlanner.winningPlan`** with `queryPlan` / `slotBasedPlan`: the part pushed into the query layer. On 9.0.4 the example above was pushed down completely (no `stages` array; `winningPlan.queryPlan` showed `GROUP` over `SORT` over `COLLSCAN`), while a pipeline ending in `$bucketAuto` showed `stages: [ { $cursor }, { $bucketAuto } ]`.
- Look for `IXSCAN` vs `COLLSCAN` in the winning plan, and `totalKeysExamined` / `totalDocsExamined` vs `nReturned`.
- Per-stage `executionTimeMillisEstimate` and `nReturned` (on the `stages` form) show where time goes.
- `usedDisk: true`, `spills` and `spilledDataStorageSize` greater than 0 mean a blocking stage exceeded its memory limit and spilled (a `$sort` with the limit lowered to 1 MB reported `usedDisk: true`, `spills: 4`; the stock limit is `memLimit: 104857600` in the plan).
- `$lookup` stages report `totalDocsExamined`, `collectionScans`, `indexesUsed`: `collectionScans > 0` means the foreign field is unindexed.

## Optimizer rewrites to recognise
Observed on 9.0.4: a `$match` written after `$project` ran at the cursor (`parsedQuery` held it); two consecutive `$match` stages were merged into one `$and`; `$sort` + `$limit` became a `LIMIT` over an index scan when an index matched; a `$match` written after `$lookup` was applied at the cursor too. The explain shows the rewritten order, not what you typed.

## Sharded clusters
Explain on a sharded cluster reports per-shard plans and where the pipeline is split; read the sharded-cluster explain section of the aggregation docs, since no sharded cluster was run for this skill.

## Fix list
1. Put an indexable `$match` first; build an index matching equality-sort-range (ESR).
2. Add `$project` early only to drop big fields before a blocking stage.
3. Index `$lookup` foreign fields.
4. `$sort` + `$limit` adjacent so top-k applies.

## Verify
Re-run explain after the fix and compare `totalDocsExamined` and total `executionTimeMillis`.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. The example pipeline ran under `explain("executionStats")`, with and without an index; all three verbosities returned plans (`allPlansExecution` showed trial stats).
- `$lookup` explain: `collectionScans: 1` with `HashJoin` for an unindexed foreign field and `collectionScans: 0` with `indexesUsed: ["_id_"]` for an indexed one; `totalDocsExamined` reported per stage. `usedDisk`/`spills`/`spilledDataStorageSize` appear in `executionStats` (set to 0/false for small inputs, non-zero when the sort limit was lowered with `internalQueryMaxBlockingSortMemoryUsageBytes`).
- Rewrites: `$match` after `$project`, merged `$match`, `$sort`+`$limit` with an index, `$match` after `$lookup` observed as written above. Fix-list items (ESR index, index on foreign field) are exercised in the reading-explain-output and lookup skills.
- The sharded paragraph was replaced with a pointer because no sharded cluster was run.
