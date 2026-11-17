---
id: computing-software.database-administration.mongodb.backup-and-point-in-time-restore
name: backup-and-point-in-time-restore
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, backup, mongodump, mongorestore, oplog, point-in-time-recovery, filesystem-snapshot, lvm-snapshot, sharded-cluster-backup, atlas-backup, percona-backup-mongodb]
level: advanced
status: docs-checked
description: "Pick filesystem snapshot vs. mongodump for MongoDB backups, and replay the oplog to restore to an exact point in time."
sources:
  - https://www.mongodb.com/docs/manual/core/backups/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MongoDB backup and point-in-time restore

**Goal:** back up a replica set or sharded cluster consistently, and know how to
restore to a specific moment, not just to "whenever the backup was taken."

## 1. mongodump/mongorestore: fine for small, wrong for large
`mongodump --oplog` captures a consistent dump of a single replica set by also
recording oplog entries during the dump and replaying them on restore
(`mongorestore --oplogReplay`) to a consistent point despite the dump itself not
being instantaneous. It is logical (BSON documents), so restoring a large dataset
means reinserting every document and rebuilding indexes. `--oplog` only works
against replica set members, not through `mongos`, and cannot be used to back up a
sharded cluster (back up sharded clusters per the manual's sharded-cluster
procedures). Fine for smaller databases, selective collection backup, or moving
data between environments; the manual points to filesystem snapshots or
Ops Manager / Cloud Manager / Atlas for larger production deployments.

## 2. Filesystem/volume snapshots: the production-scale approach
LVM, EBS, or other volume snapshots of the underlying data files, taken on a
secondary to avoid load on the primary. The manual's requirement for a correct
snapshot of a running `mongod` is that **journaling is enabled and the journal
is on the same logical volume** as the data files. Where the storage layer does not
give a point-in-time snapshot, use `db.fsyncLock()` / `fsync` with `lock: true`
to block writes while you copy, and call `fsyncUnlock` afterwards: the lock is
held until released, so a forgotten unlock leaves the node refusing writes.
A sharded cluster needs **a snapshot of every shard and a config server at
approximately the same moment**, with the balancer stopped (`sh.stopBalancer()`):
if the balancer is active while you capture backups, the artifacts may be
incomplete or contain duplicate data because chunks migrate during the backup.

## 3. Point-in-time restore via the oplog
1. Restore the base backup (whichever method).
2. Identify the target timestamp.
3. Replay oplog entries from backup time up to the target timestamp:
   `mongorestore --oplogReplay --oplogLimit <timestamp>:<increment>` against a dump
   that included `--oplog`, or reconstruct from a continuously-archived oplog
   collection if using a dedicated backup tool.
This requires the oplog window (`local.oplog.rs`, sized by
`replication.oplogSizeMB` or disk-percentage default) to still cover the backup-to
restore-target range — if the oplog has rolled over past the backup time, PITR
beyond the base backup is impossible with oplog replay alone. Size the oplog for
your longest plausible backup-to-detection gap, not just typical replication lag.

## 4. Sharded-cluster-specific traps
- Config server metadata (chunk ranges, shard assignments) must be backed up and
  restored in lockstep with shard data — restoring shards to one point and configs
  to another produces chunk ownership that doesn't match actual data placement.
- Stop the balancer (`sh.stopBalancer()`) before and during cluster-wide backup
  windows; chunks that migrate mid-backup can leave incomplete or duplicate data.

## 5. Dedicated tools
Ops Manager / Cloud Manager (MongoDB Enterprise required) back up replica sets
and sharded clusters by reading oplog data, take snapshots at set intervals and offer
point-in-time recovery; Atlas offers managed backup and restore. Prefer them over
hand-rolled mongodump/snapshot scripts once a deployment is sharded or has a real RPO
requirement.

## Verify
- [ ] Backup method matches scale: mongodump for small/selective, snapshot-based for production-scale.
- [ ] A sharded cluster's backup stops the balancer and captures all shards plus config servers within a tight time window.
- [ ] The oplog window is sized to cover the realistic backup-to-restore-target gap.
- [ ] A PITR restore has actually been drilled end-to-end, not just the base restore.
- [ ] Journaling is on and on the same volume as the data files for snapshot backups.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: filesystem snapshots need journaling on the same logical volume as the data files; sharded snapshots need the balancer stopped and every shard plus a config server captured at approximately the same moment (balancer active gives incomplete or duplicate data); fsync with lock blocks writes until released; mongodump --oplog with mongorestore --oplogReplay and --oplogLimit (<time_t>:<ordinal>), --oplog not usable on a sharded cluster or through mongos; Ops Manager / Cloud Manager (Enterprise) oplog-based snapshots with point-in-time recovery. Removed unconfirmed claims (fsyncLock auto-release, restore-time estimates, Percona Backup for MongoDB).

Method: documentation only; no commands were run.
