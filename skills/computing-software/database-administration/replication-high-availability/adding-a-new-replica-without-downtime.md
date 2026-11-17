---
id: computing-software.database-administration.replication-high-availability.adding-a-new-replica-without-downtime
name: adding-a-new-replica-without-downtime
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, replication-high-availability, new-replica, replica-provisioning, base-backup, clone, replication-setup]
level: practitioner
status: draft
description: "Add a replica to a live primary without downtime: consistent snapshot plus log position, per-engine tools (pg_basebackup, CLONE, RMAN DUPLICATE, initial sync), catch-up checks."
sources:
  - https://dataintensive.net/
  - https://www.postgresql.org/docs/current/app-pgbasebackup.html
  - https://dev.mysql.com/doc/refman/8.4/en/clone-plugin.html
  - https://www.mongodb.com/docs/manual/tutorial/expand-replica-set/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adding a new replica without downtime

## The general recipe (DDIA ch.5)
1. Take a **consistent snapshot** of the leader without locking writes.
2. Record the exact **log position** of that snapshot (LSN, GTID set, oplog timestamp, SCN).
3. Restore the snapshot on the new node.
4. Connect it to the leader and stream changes from that position until caught up.

## Per engine
**PostgreSQL**
```bash
pg_basebackup -h primary -U replicator -D /var/lib/postgresql/17/main -X stream -R -P -C -S replica3
```
`-R` writes `primary_conninfo` + `standby.signal`; `-C -S` creates a replication slot so WAL is retained during the copy. Start the server; it streams from the backup's end LSN.

**MySQL 8.0.17+**
```sql
-- on the new replica
SET GLOBAL clone_valid_donor_list = 'primary:3306';
CLONE INSTANCE FROM 'clone_user'@'primary':3306 IDENTIFIED BY '...';
-- after restart
CHANGE REPLICATION SOURCE TO SOURCE_HOST='primary', SOURCE_AUTO_POSITION=1, ...; START REPLICA;
```
GTID auto-positioning picks up from the cloned state. Alternative: Percona XtraBackup (`--backup`, `--prepare`, `xtrabackup_binlog_info` has the GTID).

**SQL Server AG**: automatic seeding (`SEEDING_MODE = AUTOMATIC`) or backup/restore WITH NORECOVERY of full + log, then join.

**Oracle**: `RMAN DUPLICATE TARGET DATABASE FOR STANDBY FROM ACTIVE DATABASE` and Data Guard broker `ADD DATABASE`.

**MongoDB**: `rs.add({host, priority: 0, votes: 0})`; initial sync copies data and applies oplog; raise priority/votes after it reaches SECONDARY. File-copy based initial sync (Enterprise) is faster for big data sets.

## Protect the primary during the copy
- Throttle (`pg_basebackup --max-rate`, xtrabackup `--throttle`) to avoid saturating disk/network.
- Ensure log retention covers the copy duration (slots, `binlog_expire_logs_seconds`, oplog window).
- Copy from an existing replica instead of the primary when possible (`pg_basebackup` from a standby, MongoDB initial sync source preference, CLONE from a replica).

## Catch-up checks before serving reads
- PostgreSQL: `pg_stat_replication` on primary shows `state = streaming` and small `replay_lag`.
- MySQL: `SHOW REPLICA STATUS\G`: both threads Running, `Seconds_Behind_Source` ≈ 0.
- MongoDB: member `SECONDARY` and lag near 0.
Add to the load balancer only after this.

## Verify
Checksums or row counts on key tables match (pt-table-checksum, `pg_checksums` for files, `dbHash` in MongoDB) and the replica appears in monitoring with lag alerts.
