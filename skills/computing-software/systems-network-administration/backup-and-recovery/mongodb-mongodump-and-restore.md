---
id: computing-software.systems-network-administration.backup-and-recovery.mongodb-mongodump-and-restore
name: mongodb-mongodump-and-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [mongodump, mongorestore, mongodb, database-backup, oplog, point-in-time-recovery]
level: practitioner
status: docs-checked
description: "Back up MongoDB with mongodump/mongorestore (oplog for consistency, archive and gzip, secondaries) and know when filesystem snapshots or Ops Manager/Atlas backup are required."
sources:
  - https://www.mongodb.com/docs/database-tools/mongodump/
  - https://www.mongodb.com/docs/database-tools/mongorestore/
  - https://www.mongodb.com/docs/manual/core/backups/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MongoDB backups with mongodump

**Goal:** consistent MongoDB logical backups for small/medium replica sets, and the right method for bigger or sharded clusters.

## Replica set dump (point-in-time consistent)
```sh
mongodump --uri "mongodb://backup:***@rs1a,rs1b,rs1c/?replicaSet=rs1&authSource=admin" \
  --readPreference=secondary --oplog --gzip --archive=/backup/rs1-$(date +%F).archive.gz
```
- `--oplog` takes a point-in-time snapshot on a replica set that is not part of a sharded cluster, and captures the writes made during the dump. It cannot be combined with `--db`, and mongodump refuses it when connected to a mongos.
- The built-in roles for this are `backup` (for mongodump) and `restore` (for mongorestore).

## Restore
```sh
mongorestore --uri "mongodb://admin:***@newhost/?authSource=admin" \
  --gzip --archive=/backup/rs1-2026-10-17.archive.gz --oplogReplay --drop
mongorestore ... --nsInclude 'shop.orders' --nsFrom 'shop.*' --nsTo 'shop_restore.*'   # partial / renamed
```
`--drop` drops each collection before restoring it.
## When not to use mongodump
- **Sharded clusters**: `--oplog` is not available through mongos. The MongoDB manual says sharded cluster snapshots are hard to achieve with other methods and points to Cloud Manager or Ops Manager (which read the oplog and offer point-in-time recovery), or to filesystem snapshots taken from every shard (and the config servers) with the balancer disabled (`sh.stopBalancer()`).
- Large datasets: choose a snapshot-based method; the manual lists Cloud Manager, Ops Manager, filesystem snapshots and mongodump as the options.

## Filesystem snapshots
To get a correct snapshot of a running `mongod`, journaling must be enabled and the journal must be on the same volume as the data files (LVM and EBS snapshots are the manual's examples). `db.fsyncLock()` flushes pending writes and locks the server against writes until `db.fsyncUnlock()`.

## Gotchas
- mongodump and mongorestore ship in the separately versioned Database Tools package; check the tools' compatibility list against your server version.

## Verify
Restore into a scratch instance, compare `db.collection.countDocuments()` for key collections, and run an application smoke query.

## Checked

Checked 2026-10-27 against the MongoDB manual sources in mongodb/docs (core/backups, built-in roles, db.fsyncLock) and the mongo-tools source in mongodb/mongo-tools (mongodump and mongorestore options and error handling). Confirmed: `--oplog` semantics and its rejection with `--db` and on a mongos, `--gzip`, `--archive`, `--readPreference`, mongorestore `--oplogReplay`, `--drop`, `--nsInclude`, `--nsFrom` and `--nsTo`, the `backup` and `restore` built-in roles, the journal-on-same-volume requirement for filesystem snapshots, balancer disabling for sharded snapshots, and `db.fsyncLock()`. Removed the unconfirmed dataset-size and cache-eviction remarks and the third-party Percona tool mention.

Method: documentation only; no commands were run.
