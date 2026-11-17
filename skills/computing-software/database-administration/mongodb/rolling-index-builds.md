---
id: computing-software.database-administration.mongodb.rolling-index-builds
name: rolling-index-builds
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-indexes, rolling-index-build, index-build, createindexes, commitquorum, replica-set-maintenance, currentop-index-build]
level: practitioner
status: docs-checked
description: "Build indexes on large MongoDB collections safely: how simultaneous replica-set builds work, commitQuorum, monitoring, and rolling builds member by member."
sources:
  - https://www.mongodb.com/docs/manual/core/index-creation/
  - https://www.mongodb.com/docs/manual/tutorial/build-indexes-on-replica-sets/
  - https://www.mongodb.com/docs/manual/reference/command/createIndexes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Index builds on populated collections and rolling builds

**Goal:** add an index to a big production collection without stalling writes or lagging secondaries.

## Default: simultaneous build
```javascript
db.orders.createIndex({ customerId: 1, createdAt: -1 }, { name: "cust_created", commitQuorum: "votingMembers" })
```
- Replica set and sharded builds run simultaneously on all data-bearing members; an exclusive collection lock is held only briefly at the start and end, and the rest yields to reads and writes. Needs featureCompatibilityVersion 4.4 or higher on every `mongod`.
- `commitQuorum` is the minimum number of data-bearing voting members (including the primary) that must be ready to commit before the primary commits the index. Default `votingMembers` (all data-bearing voting members). If one of them is unreachable, the build can hang until it returns. Relax an in-progress build with the `setIndexCommitQuorum` command.
- Memory (self-hosted): `maxIndexBuildMemoryUsageMegabytes` defaults to 200 MB per `createIndexes` command, shared equally among its indexes, then temporary files are written under `_tmp` in the dbPath. `maxNumActiveUserIndexBuilds` defaults to 3, so total memory can reach three times that. Consider a maintenance window with reduced writes.

## Monitor and abort
```javascript
db.currentOp({ $or: [ { op: "command", "command.createIndexes": { $exists: true } }, { op: "none", "msg": /^Index Build/ } ] })
db.orders.dropIndex("cust_created")        // terminates an in-progress build
```
The `msg` field gives a percentage complete for the current stage. Key constraint violations make the primary abort the build.

## Rolling build (only when the default is too heavy)
The manual says to use it only if average CPU utilisation exceeds (N-1)/N-10% (N = CPU threads available to `mongod`), or the WiredTiger cache fill ratio regularly exceeds 90%. It lowers cluster resiliency and lengthens the build, and must not run concurrently with a replicated index build. This procedure is for replica sets; sharded clusters have their own procedure in the manual. For each secondary, one at a time:
1. On the primary, set that member's `priority` to 0 and `hidden` to true, then `rs.reconfig(cfg)` (record the original priority).
2. Restart it as a standalone: remove `replication.replSetName` (or `--replSet`), use a different port, and set `disableLogicalSessionCacheRefresh: true`.
3. Connect to that port and run `createIndex()`.
4. Restart it as a member again (original port and replica set name, remove `disableLogicalSessionCacheRefresh`) and let it catch up.
5. Unhide it and restore its priority with `rs.reconfig()`.
Finally `rs.stepDown()` the primary and repeat on it.

The oplog must be large enough for each member to catch up after its build.

## Unique indexes
The rolling procedure for a unique index requires stopping all writes to the collection for its duration, otherwise members can end up inconsistent. If you cannot stop writes, build the unique index with `createIndex()` on the primary instead.

## Verify
`db.orders.getIndexes()` on every member shows the index; check replica lag stayed within your target during the build.

## Checked
2026-10-31. Against the MongoDB manual pages Index Builds on Populated Collections, Create a Rolling Index Build on Replica Sets and createIndexes: locking behaviour, FCV 4.4 requirement, `commitQuorum` default and hang risk, `setIndexCommitQuorum`, 200 MB memory default and `_tmp`, `maxNumActiveUserIndexBuilds` default 3, `dropIndex()` terminating a build, the rolling-build criteria and steps, and the unique-index condition. Removed or corrected: the claim that rolling unique builds are unsafe (the manual allows them with writes stopped), `ttlMonitorEnabled`, the Atlas rolling option, sharded balancer advice, `rs.printSecondaryReplicationInfo()` and `$group` duplicate-check recipe.
Method: documentation only; no commands were run.
