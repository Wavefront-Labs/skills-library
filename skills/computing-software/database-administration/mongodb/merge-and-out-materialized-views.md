---
id: computing-software.database-administration.mongodb.merge-and-out-materialized-views
name: merge-and-out-materialized-views
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, aggregation-pipeline, merge-stage, out-stage, on-demand-materialized-view, whenmatched, incremental-rollup, reporting-collection]
level: practitioner
status: verified
description: "Build incremental on-demand materialized views in MongoDB with $merge (whenMatched/whenNotMatched) and full rebuilds with $out, and schedule refreshes."
sources:
  - https://www.mongodb.com/docs/manual/core/materialized-views/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/merge/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/out/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $merge / $out materialized views

**Goal:** fast dashboards that read precomputed rollups instead of aggregating raw events on every request.

## Incremental rollup with $merge
```javascript
function refreshDaily(since) {
  db.orders.aggregate([
    { $match: { updatedAt: { $gte: since } } },
    { $group: { _id: { day: { $dateTrunc: { date: "$createdAt", unit: "day" } }, region: "$region" },
                revenue: { $sum: "$total" }, orders: { $sum: 1 } } },
    { $merge: { into: "daily_revenue", on: "_id",
                whenMatched: "replace",          // or "merge", "keepExisting", "fail", or a pipeline
                whenNotMatched: "insert" } }
  ]);
}
```
Recompute only affected keys (days touched since the last run) and `replace` them; `whenMatched: [ { $set: { revenue: { $add: ["$revenue", "$$new.revenue"] } } } ]` adds deltas but is not idempotent if a run is retried.

`on` fields must have a unique index on the target (`_id` always does): `db.daily_revenue.createIndex({ day: 1, region: 1 }, { unique: true })` if merging on those.

## Full rebuild with $out
```javascript
db.orders.aggregate([ ..., { $out: "daily_revenue" } ])          // atomically replaces the collection
db.orders.aggregate([ ..., { $out: { db: "reporting", coll: "daily_revenue" } } ])   // other database
```
Writes to a temp collection then renames: readers see old or new, never partial. Indexes on the target are preserved.

## $merge vs $out
| | $merge | $out |
|---|---|---|
| Existing data | Kept, merged per document | Replaced entirely |
| Other database | Yes | Yes |
| Same collection as source | Yes (`$merge` into the input collection ran; be careful) | Ran without error on 9.0.4 and replaced the collection; avoid |

## Scheduling
Run from a cron job / Atlas Scheduled Trigger; store the last-run watermark in a small `etl_state` collection; use `updatedAt` indexed on the source.

## Gotchas
- `$merge`/`$out` must be the last stage ("$merge can only be the final stage"); `$merge` is rejected inside `$facet` and inside a `$lookup` sub-pipeline.
- `$merge` is New in 5.0; the docs say it can run on secondary nodes when all nodes are on a recent featureCompatibilityVersion, while the writes still go to the primary.
- Writes count as normal writes: large rebuilds generate oplog volume and replica lag.

## Verify
Totals in `daily_revenue` for a sample day equal a live `$group` over `orders` for that day; a second identical refresh run changes nothing.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. The `refreshDaily` function ran twice (second run left 1 document, so `replace` is idempotent); the delta pipeline with `$$new.revenue` doubled the revenue (11 to 22), confirming it is not idempotent on retry; `on` without a unique index errors ("Cannot find index to verify that join fields will be unique") and works after a unique index.
- `$out` replaced the target and kept its secondary index; `$out` to another database worked; `$merge` not last, in `$facet` and in `$lookup` errored. `$out` and `$merge` into the source collection both ran.
- Docs fetched: `$merge` page (New in version 5.0; can run on secondaries). The sharded-target and 4.4/5.1 gates in the table were not confirmed and were removed.
