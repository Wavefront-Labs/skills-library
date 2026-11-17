---
id: computing-software.database-administration.mongodb.oplog-sizing-and-replication-window
name: oplog-sizing-and-replication-window
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, replica-set, oplog-size, replication-window, replsetresizeoplog, oplog-min-retention-hours, initial-sync, replication-lag]
level: practitioner
status: docs-checked
description: "Size the MongoDB oplog so the replication window covers maintenance and lag: measure it, resize online with replSetResizeOplog, and set minimum retention."
sources:
  - https://www.mongodb.com/docs/manual/core/replica-set-oplog/
  - https://www.mongodb.com/docs/manual/tutorial/change-oplog-size/
  - https://www.mongodb.com/docs/manual/reference/command/replSetResizeOplog/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Oplog sizing and replication window

**Goal:** a secondary that is down for maintenance, or lagging, can always catch up from the oplog instead of needing a full initial sync.

## Measure the window
```javascript
rs.printReplicationInfo()
// configured oplog size:   51200MB
// log length start to end: 172800secs (48hrs)
db.getReplicationInfo().timeDiffHours
```
Window = time span currently in the oplog. It shrinks during write bursts (bulk loads, big migrations).

## Target
Window >= longest planned outage (patch, rolling index build, backup restore test) + headroom; 24-72 h is common. Check during your heaviest write period, not overnight.

## Resize online (each member, no restart)
```javascript
use local
db.oplog.rs.stats().maxSize                              // bytes
db.adminCommand({ replSetResizeOplog: 1, size: Double(102400) }) // MB, minimum 990; Double() required in mongosh
db.adminCommand({ replSetResizeOplog: 1, minRetentionHours: 48 })  // keep at least 48 h even if over size
```
Set on every member (secondaries first). Shrinking does not return disk space automatically; run `compact` on `local.oplog.rs` to reclaim it (no benefit after increasing the size). A member cannot replicate oplog entries while `compact` runs on `oplog.rs`, so schedule it in a maintenance window and never run it on the primary (step it down first).
Config file equivalent: `replication.oplogSizeMB` (only at first startup) and `storage.oplogMinRetentionHours`.

## Defaults
WiredTiger: 5% of free disk space, minimum 990 MB, maximum 50 GB (64-bit macOS: 192 MB). The in-memory engine uses 5% of physical memory. `minRetentionHours` only removes an entry once the oplog has reached its maximum size and the entry is older than the retention period, so the oplog can grow beyond its size cap: watch disk.

## Reading lag against window
```javascript
rs.printSecondaryReplicationInfo()   // syncedTo and behind-the-primary per secondary
```
A secondary that falls behind the end of the oplog becomes stale and needs a full resync.

## Gotchas
- Multi-document updates are translated into one oplog operation per document, which can use a great deal of oplog space; deletes roughly equal to inserts and many in-place updates also generate large oplogs without data growth.

## Verify
`db.getReplicationInfo().timeDiffHours` meets the target at the end of a peak write day.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: WiredTiger default oplog 5% of free disk with 990 MB minimum and 50 GB maximum (192 MB on 64-bit macOS), replSetResizeOplog size (minimum 990 MB, Double() in mongosh) and minRetentionHours without restart, oplogMinRetentionHours semantics, oplogSizeMB effective only at oplog creation, compact on oplog.rs on a secondary blocks replication, rs.printReplicationInfo and getReplicationInfo().timeDiffHours, multi-updates become one oplog op per document. Removed unconfirmed alert threshold, retryable-write and large-entry claims, and the RECOVERING state attribution.

Method: documentation only; no commands were run.
