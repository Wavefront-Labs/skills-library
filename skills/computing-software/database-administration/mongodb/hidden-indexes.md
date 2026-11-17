---
id: computing-software.database-administration.mongodb.hidden-indexes
name: hidden-indexes
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-indexes, hidden-index, hideindex, unhideindex, index-removal, index-usage-stats, indexstats]
level: practitioner
status: verified
description: "Safely evaluate dropping a MongoDB index by hiding it from the planner (hideIndex/unhideIndex), using $indexStats evidence, then drop or restore instantly."
sources:
  - https://www.mongodb.com/docs/manual/core/index-hidden/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/indexStats/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hidden indexes

**Goal:** remove an index you think is unused without risking hours of rebuild if you were wrong.

## 1. Find candidates
```javascript
db.orders.aggregate([ { $indexStats: {} }, { $project: { name: 1, "accesses.ops": 1, "accesses.since": 1 } } ])
```
`accesses.ops` counts since the last restart (`since`) on THIS member only: run it on every member, including secondaries serving reads, and after a long enough uptime to cover monthly jobs.

Also check for overlapping indexes: `{a:1}` is redundant if `{a:1, b:1}` exists.

## 2. Hide
```javascript
db.orders.hideIndex("status_1")          // or db.runCommand({ collMod: "orders", index: { name: "status_1", hidden: true } })
db.orders.getIndexes()                   // shows hidden: true
```
The planner ignores it, but it is still maintained on writes and still enforces `unique` and TTL. Replicates to secondaries; persists across restarts.

## 3. Watch
Profiler/slow logs, `planSummary: COLLSCAN` spikes, p95 latency, Atlas Performance Advisor. Keep it hidden through at least one full business cycle.

## 4. Decide
```javascript
db.orders.unhideIndex("status_1")        // instant rollback
db.orders.dropIndex("status_1")          // when confident
```

## Gotchas
- Cannot hide the `_id` index ("can't hide _id index") or a clustered index.
- `hint()` on a hidden index errors ("hint provided does not correspond to an existing index"); check code for hints first.
- Hidden indexes still cost write I/O and RAM; hiding is a trial, not the end state.
- Hidden indexes need a recent featureCompatibilityVersion; confirm the exact minimum in the hidden-index docs for older servers.

## Verify
After hiding, `explain()` of the formerly-served query shows a different plan; latency stays within SLO.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. `$indexStats` listed the three indexes; `hideIndex("status_1")` and `collMod ... hidden: true` both returned `hidden_new: true`; `getIndexes()` shows `hidden: true`; the same query went from IXSCAN to `COLLSCAN`; `unhideIndex` restored it.
- A hidden unique index still raised E11000 on a duplicate insert. TTL and text indexes can also be hidden. `hideIndex("_id_")` errors.
- Docs fetched: hidden-index and `$indexStats` pages. The "4.4+" feature gate was not confirmed from the current docs and was reworded.
