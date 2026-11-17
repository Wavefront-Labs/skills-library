---
id: computing-software.database-administration.mongodb.reclaiming-disk-space-with-compact
name: reclaiming-disk-space-with-compact
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-administration, compact-command, disk-space, wiredtiger, autocompact, initial-sync]
level: practitioner
status: gated
description: "Reclaim disk after large MongoDB deletes: measure reusable space, run compact (or autoCompact in 8.0) member by member, or resync a member from scratch."
sources:
  - https://www.mongodb.com/docs/manual/reference/command/compact/
  - https://www.mongodb.com/docs/manual/reference/command/autoCompact/
  - https://www.mongodb.com/docs/manual/tutorial/resync-replica-set-member/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reclaiming disk space (compact / resync)

WiredTiger reuses space freed by deletes inside its files but does not return it to the OS.
After a big purge you may want the disk back.

## Measure reusable space
```js
db.orders.stats().wiredTiger["block-manager"]["file bytes available for reuse"]
db.orders.stats({ scale: 1024 * 1024 })          // storageSize vs size (MB)
// per index
db.orders.stats({ indexDetails: true }).indexDetails["status_1"]["block-manager"]["file bytes available for reuse"]   // indexDetails is off by default
```
Only bother if "available for reuse" is a large share of `storageSize` and the collection
won't grow back soon.

## compact
```js
db.runCommand({ compact: "orders" })                 // run on each member, not via mongos
db.runCommand({ compact: "orders", dryRun: true })   // New in 8.0: returns estimatedBytesFreed
```
- Per the docs `compact` does not block CRUD operations, but it temporarily changes WiredTiger's block-manager strategy, which can slow checkpoints and transaction commits on that member. It cannot be run against `mongos`.
- Run on **secondaries first**, one at a time, then step down the primary and compact it.
- Resize the oplog with `replSetResizeOplog` (replica set members only: it errors with "oplog does not exist" on a standalone).
- Results vary: compact on a collection with 27,000 of 30,000 documents deleted returned `bytesFreed: 0` in the test.

## autoCompact (New in 8.0)
```js
db.adminCommand({ autoCompact: true, freeSpaceTargetMB: 1024 })    // background, per node
```
Runs compaction continuously on files with at least that much free space; consider for
workloads with regular purges.

## Resync instead (gated: unconfirmed, source is paywalled or blocked)
This procedure and the TTL/time-series advice below were not run here.

For very fragmented members, an **initial sync** produces fresh compact files:
1. Stop the secondary, empty its dbPath, start it: it resyncs from another member.
2. Or seed it from a snapshot of a compacted member.
Needs an oplog window longer than the sync takes; do one member at a time.

## Prevent bloat
- Use TTL indexes or drop whole collections/partitions-by-collection for time-based purges
  (dropping a collection frees files immediately).
- Time series collections expire whole buckets.

## Verify
Filesystem usage (`df -h` on dbPath) drops on the member, and
`file bytes available for reuse` falls; replication lag returned to normal after the operation.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. 30,000 documents (about 500 bytes each) with an index; after `deleteMany` of 27,000 and a checkpoint (`fsync`), `stats({indexDetails: true})` gave `storageSize` 184320 and index `k_1` "file bytes available for reuse" 151552; without `indexDetails: true` the `indexDetails` field is absent (the original snippet failed with undefined). `stats({scale: 1048576})` returned MB. `wiredTiger["block-manager"]["file bytes available for reuse"]` is present.
- `compact` returned `{bytesFreed: 0}`, `compact` with `dryRun: true` returned `{estimatedBytesFreed: 0}`, `autoCompact: true, freeSpaceTargetMB: 1024` and `autoCompact: false` returned ok on a standalone. `replSetResizeOplog` errors on a standalone.
- Docs fetched: compact command page (`dryRun` New in 8.0; does not block CRUD; not on mongos), autoCompact page (New in 8.0). The initial-sync/resync and TTL advice are procedures not exercised here.
