---
id: computing-software.database-administration.mongodb.reading-explain-output
name: reading-explain-output
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, compound-index, mongodb-explain, collscan, ixscan, executionstats, query-planner]
level: practitioner
status: verified
description: "Read MongoDB explain('executionStats') output: winning plan stages, keys vs docs examined vs returned, in-memory SORT, rejected plans and plan cache behaviour."
sources:
  - https://www.mongodb.com/docs/manual/reference/explain-results/
  - https://www.mongodb.com/docs/manual/tutorial/analyze-query-plan/
  - https://www.mongodb.com/docs/manual/core/query-plans/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading explain output

```js
db.orders.find({ customerId: 42, status: "open" }).sort({ createdAt: -1 }).limit(20)
  .explain("executionStats")
db.orders.explain("allPlansExecution").aggregate([...])
```
Verbosity: `queryPlanner` (plan only), `executionStats` (runs the winning plan), `allPlansExecution`
(also trial stats of rejected plans).

## Winning plan stages (read bottom-up)
| Stage | Meaning |
|---|---|
| `COLLSCAN` | full collection scan |
| `IXSCAN` | index scan; check `indexName`, `keyPattern`, `indexBounds` |
| `FETCH` | fetch full documents for keys found |
| `SORT` | **in-memory sort** (blocking; `memLimit` 104857600 = 100 MB in the plan) |
| `PROJECTION_COVERED` | answered from the index alone (no FETCH) |
| `SUBPLAN`, `OR` | `$or` planned per clause, then index scans combined (seen for `$or` over two indexes) |
| `LIMIT` | applied above an index scan when sort and filter are served by the index |
On 9.0.4 an aggregation pushed into the slot-based engine shows `queryPlan` and `slotBasedPlan` under `winningPlan` with stages such as `GROUP`, `SORT` (with `memLimit: 104857600`) and `COLLSCAN`.

## The three numbers
In `executionStats`:
- `nReturned`
- `totalKeysExamined`
- `totalDocsExamined`
Ideal: keys ~= docs ~= returned. `docsExamined` >> `nReturned` means the index does not cover
the filter (documents fetched then discarded); keys >> returned means poor selectivity or range
before equality in the index. `executionTimeMillis` and per-stage `executionTimeMillisEstimate`
show where time goes.

## Fixing with the ESR rule
Index fields in order **Equality, Sort, Range**: for the query above,
`{ customerId: 1, status: 1, createdAt: -1 }` gives IXSCAN with no SORT stage and keys
examined = 20.

## Rejected plans and the plan cache
The planner races candidate plans for a trial period and caches the winner per **query shape**.
A cached plan good for one parameter can be bad for another (skew). Inspect and reset:
```js
db.orders.getPlanCache().list()
db.orders.getPlanCache().clear()
```
Force an index for testing: `.hint({ customerId: 1, status: 1, createdAt: -1 })`.
Query settings (`setQuerySettings`) and index filters pin index choices persistently; `setQuerySettings` is rejected on a standalone ("can only run on replica sets or sharded clusters"), so test it on a replica set.

## Gotchas
- `explain()` on `count()` / `distinct()` / `update` needs `db.collection.explain().update(...)` form.
- For slow queries already logged, the log line (`planSummary`, `keysExamined`, `docsExamined`)
  gives the same signals without re-running.

## Verify
After adding the right index, `executionStats` shows IXSCAN on it, no SORT stage, and
keys/docs examined close to nReturned.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. 5000 orders. Without an index the query shows `SORT` over `COLLSCAN` (20 returned, 5000 docs examined). After `{ customerId: 1, status: 1, createdAt: -1 }` it shows `LIMIT`/`FETCH`/`IXSCAN` with no `SORT`, keys 20, docs 20, returned 20. A projection of indexed fields gave `PROJECTION_COVERED` with no `FETCH`.
- `allPlansExecution` returned `executionStats.allPlansExecution` (2 plans) and one rejected plan; `$or` over two indexes gave `SUBPLAN` > `OR`; `getPlanCache().list()` returned a cached shape and `clear()` emptied it; `hint` forced the index; `explain().count()`, `.distinct()` and `.update()` all work (deprecated `update` warns).
- Slow log lines (`attr.planSummary`, `keysExamined`, `docsExamined`, `nreturned`, `durationMillis`) were read from the mongod JSON log with Python. Sharded stage names (`SHARD_MERGE`, `SINGLE_SHARD`) and `SORT_MERGE` were removed because they were not run.
