---
id: computing-software.database-administration.mongodb.mongostat-mongotop-and-serverstatus
name: mongostat-mongotop-and-serverstatus
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-production-notes, mongodb-administration, mongostat, mongotop, serverstatus, opcounters, connections, replication-lag, live-monitoring]
level: practitioner
status: verified
description: "Watch a live MongoDB deployment with mongostat, mongotop and db.serverStatus(): which columns matter (ops, dirty/used cache, queues, connections) and what bad values look like."
sources:
  - https://www.mongodb.com/docs/database-tools/mongostat/
  - https://www.mongodb.com/docs/database-tools/mongotop/
  - https://www.mongodb.com/docs/manual/reference/command/serverStatus/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mongostat, mongotop and serverStatus

**Goal:** in the first minutes of an incident, see whether the node is
overloaded, which collections are hot, and whether replication keeps up.

## mongostat: per-second server counters
```bash
mongostat --uri "mongodb://monitor@db1:27017/?authSource=admin" --discover 5
```
`--discover` shows every replica set member; columns to read:
| Column | Meaning / red flag |
|---|---|
| insert query update delete getmore command | Operation rates; sudden drop with steady load = stall |
| dirty / used | WiredTiger cache % dirty / used: dirty > 20% or used > 95% = eviction pressure |
| flushes | Checkpoints per interval |
| qrw / arw | Queued / active readers-writers: sustained queues = saturation |
| conn | Open connections: climbing = pool leak or retry storm |
| set / repl | Replica set name and the member's replication status code (see the mongostat docs table); `--discover` adds a `host` column |

## mongotop: time spent per collection
```bash
mongotop --uri "mongodb://monitor@db1:27017/?authSource=admin" 5
```
Shows read/write milliseconds per namespace per interval: identifies the hot
collection to profile next.

## serverStatus: the source of both
```javascript
const s = db.serverStatus();
({ uptime: s.uptime, conns: s.connections, ops: s.opcounters,
   queues: s.globalLock && s.globalLock.currentQueue,
   tickets: s.queues && { read: s.queues.execution.read.normalPriority, write: s.queues.execution.write.normalPriority },   // out / available / totalTickets
   asserts: s.asserts, net: s.network })
rs.printSecondaryReplicationInfo()    // lag per secondary (errors on a standalone)
```
Monitoring tools read `serverStatus`; alert on connections, queue length, cache dirty %, replication lag and asserts.

## Monitoring user
```javascript
db.getSiblingDB("admin").createUser({ user: "monitor", pwd: passwordPrompt(), roles: [ { role: "clusterMonitor", db: "admin" } ] })
```

## Gotchas
- Counters are cumulative since start in serverStatus; compute rates between samples.

## Verify
During a load test, mongostat op rates and mongotop hot collections match the
expected workload, and exporter dashboards show the same values.

## Checked
- MongoDB 9.0.4 Community, mongosh 2.13.0 and Database Tools 100.19.1 (mongostat, mongotop) on Windows, run in a scratch folder. `mongostat --rowcount 2 1` printed the columns insert, query, update, delete, getmore, command, dirty, used, flushes, vsize, res, qrw, arw, net_in, net_out, conn, time; with `--discover` against a two-member set it added `host`, `set` and `repl`. `mongotop --rowcount 1 2` printed `ns`, `total`, `read`, `write` per namespace.
- On 9.0.4 `serverStatus().wiredTiger.concurrentTransactions` does not exist (the original ticket line returned undefined); tickets are under `serverStatus().queues.execution.read/write.normalPriority` (out, available, totalTickets: 0, 12, 12). `connections`, `opcounters`, `globalLock.currentQueue`, `asserts`, `network` exist. `rs.printSecondaryReplicationInfo()` printed `replLag: "0 secs"` on a primary with one secondary and errors on a standalone. `createUser` with `clusterMonitor` succeeded.
- Docs fetched: mongostat page (the `repl` column; there is no `lag` column in the docs). The 20% dirty and 95% used thresholds match the WiredTiger eviction trigger defaults (see the wiredtiger-cache-sizing skill). The mongos remark was removed as unconfirmed.
