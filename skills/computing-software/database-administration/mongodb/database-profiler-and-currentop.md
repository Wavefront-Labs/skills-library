---
id: computing-software.database-administration.mongodb.database-profiler-and-currentop
name: database-profiler-and-currentop
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-production-notes, mongodb-administration, database-profiler, currentop, slowms, killop, slow-queries, system-profile, plansummary]
level: practitioner
status: verified
description: "Find slow MongoDB operations with the slow-query log and database profiler (slowms, sampleRate), inspect running ones with $currentOp, and kill runaways with killOp."
sources:
  - https://www.mongodb.com/docs/manual/tutorial/manage-the-database-profiler/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/currentOp/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiler and currentOp

**Goal:** name the queries that are slow (historically and right now) and stop
one that is hurting the cluster.

## Slow query log (always on)
Operations slower than `slowms` (100 ms default) are logged to the mongod log
regardless of profiling level:
```javascript
db.setProfilingLevel(0, { slowms: 50, sampleRate: 1.0 })   // level 0 = log only, no system.profile
```
Log lines (JSON) include `planSummary` (`COLLSCAN` = no index), `keysExamined`,
`docsExamined`, `nreturned`, `durationMillis`. Find the worst:
```python
# python -I slowq.py mongod.log   (stdlib only; jq is not needed)
import json, sys
rows = []
for line in open(sys.argv[1], encoding="utf8"):
    if '"Slow query"' in line:
        a = json.loads(line)["attr"]
        rows.append((a["durationMillis"], a["ns"], a.get("planSummary")))
for r in sorted(rows, reverse=True)[:10]:
    print(*r, sep="\t")
```

## Database profiler (per database, writes to system.profile)
```javascript
use shop
db.setProfilingLevel(1, { slowms: 50 })            // 1 = slow ops, 2 = all ops (only briefly)
db.system.profile.find({ millis: { $gt: 200 } }).sort({ ts: -1 }).limit(5).pretty()
db.system.profile.aggregate([{ $group: { _id: { ns: "$ns", plan: "$planSummary" }, n: { $sum: 1 }, avg: { $avg: "$millis" } } }, { $sort: { n: -1 } }])
db.setProfilingLevel(0)
```
`system.profile` is a capped collection of 1,048,576 bytes by default; profiling adds write
load. Profile each mongod (the tutorial runs it per database on a mongod). Atlas has its own Query Profiler.

## Running operations
```javascript
db.getSiblingDB("admin").aggregate([
  { $currentOp: { allUsers: true, idleConnections: false } },
  { $match: { secs_running: { $gt: 10 }, op: { $ne: "none" } } },
  { $project: { opid: 1, secs_running: 1, ns: 1, op: 1, planSummary: 1, command: 1, client: 1 } } ])
db.killOp(<opid>)
```
On sharded clusters see the `$currentOp` docs for `localOps` and for killing operations through mongos (not run here, no sharded cluster).

## Fix loop
`COLLSCAN` or `docsExamined` >> `nreturned` → add/adjust an index (ESR rule),
then confirm with `explain("executionStats")`. Set `maxTimeMS` on app queries to cap runaways.

## Gotchas
- Don't kill internal ops (replication, balancer, index builds) blindly: check `desc` and `op`.
- Profiler level 2 on a busy primary can measurably slow it.

## Verify
After the fix, the query's log lines disappear from the slow log (or show IXSCAN and low docsExamined).

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. `setProfilingLevel(0, {slowms: 50, sampleRate: 1.0})` and `setProfilingLevel(1, {slowms: 0})` returned the previous settings; `system.profile` rows had `op`, `planSummary` (`COLLSCAN` and the `IXSCAN` key pattern), `millis`, `docsExamined`, `keysExamined`, `nreturned`; the `$group` over `system.profile` ran; `system.profile` is capped with `maxSize: 1048576`; level 2 and back to 0 worked.
- A `$where` sleep query was listed by the `$currentOp` pipeline (`op: query`, `planSummary: COLLSCAN`, `secs_running` 4) and `db.killOp(opid)` returned "attempting to kill op", after which the client got "kill pending". A `comment` set on an aggregate appeared as `command.comment` in `system.profile`.
- The mongod JSON log contains "Slow query" lines whose `attr` has `durationMillis`, `ns`, `planSummary`, `keysExamined`, `docsExamined`, `nreturned` (read with the Python snippet; `jq` is not installed here, so the original `jq` pipeline was replaced).
- Not run: sharded `$currentOp`/`killOp` through mongos (pointer only).
