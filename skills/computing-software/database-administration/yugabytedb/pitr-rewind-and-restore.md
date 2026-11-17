---
id: computing-software.database-administration.yugabytedb.pitr-rewind-and-restore
name: pitr-rewind-and-restore
category: computing-software
field: database-administration
product: yugabytedb
tags: [pitr, restore-snapshot-schedule, rewind, restore-to-point-in-time, list-snapshot-restorations, ddl, cdc]
level: advanced
status: docs-checked
description: "Rewind a database in place with restore_snapshot_schedule to a timestamp or relative time, and the caveats around DDL, partial indexes and CDC streams."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/backup-restore/point-in-time-recovery/rewind.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/backup-restore/point-in-time-recovery/restore.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PITR rewind and restore

Restore a database in place to an earlier time, using its snapshot schedule.

```
yb-admin --master_addresses <masters> restore_snapshot_schedule <schedule_id> <timestamp>
yb-admin --master_addresses <masters> restore_snapshot_schedule <schedule_id> minus 5m
yb-admin --master_addresses <masters> restore_snapshot_schedule <schedule_id> minus 1h
yb-admin --master_addresses <masters> list_snapshot_restorations
```
The timestamp can be a Unix timestamp in microseconds, a YSQL or YCQL timestamp (for example "2022-05-01 13:00-0700"), or relative (`minus 5m`). Prerequisites: a snapshot schedule exists for the database or keyspace, and no rewind or restore is already running for it (concurrent commands can leave the data inconsistent).

Restore to PIT is a different, lower-level workflow that starts from a snapshot rather than the live database: `yb-admin restore_snapshot <snapshot-id> [<restore-target>]`, where the optional target is at or before the snapshot's creation time (absolute microseconds or `minus 5m`). It does not check that the target is recoverable, so prefer rewind or clone to PIT for in-cluster recovery. You cannot restore to a time earlier than the most recent DDL change that precedes the snapshot, and a single snapshot cannot recover data outside its history retention window.

Rules and effects:
- Rewind restores the whole database (schema and data) to the target time on the original cluster. Issuing DDL while a rewind runs is not recommended, and rewinding to a time when DDL was in flight may fail or give inconsistent results. You cannot rewind to before the most recent YSQL system catalog upgrade.
- Data written after the target time is permanently discarded from that database. Use rewind only when there were no important writes after the error or they can be replayed; otherwise use clone to PIT or restore to PIT.
- Rewind does not restore global objects (tablespaces, roles, permissions), `DROP TABLESPACE` is disallowed while a schedule exists, and PITR is not supported for databases with vector indexes.
- With xCluster, PITR commands are not replicated: stop workloads, wait for replication to finish, delete xCluster replication on both clusters, rewind both to the exact same time, re-establish replication and resume.
- YSQL only: indexes that were part-way through a backfill at the target time appear in `pg_index` with `NOT indisvalid`; drop and recreate them.
- CDC streams and replication slots must be recreated after a rewind.
- For restore_snapshot, check progress with `list_snapshots` or `list_snapshot_restorations` (a finished restoration shows state RESTORED; FAILED is also possible).
- Under encryption at rest, restoring distributed snapshots of an encrypted cluster to a new cluster needs the keys used for encryption, including rotated keys, copied to the new cluster.
- On a YugabyteDB Anywhere universe manage PITR only from its UI; a database or keyspace can have at most one snapshot schedule and yb-admin changes are not reflected in the UI.

## Checked

2026-11-04. Confirmed against the Rewind to PIT page (restore_snapshot_schedule forms and timestamp formats, prerequisites, index backfill note and query, CDC, xCluster, global objects, system catalog upgrade, YugabyteDB Anywhere warning, DDL and vector index limits), the Restore to PIT page (restore_snapshot with optional target, DDL boundary and retention warnings, progress check), the yb-admin reference (list_snapshot_restorations state RESTORED or FAILED) and the Encryption at rest page (keep rotated keys). Corrected the DDL line: rewind restores schema as well as data; the real limits are in-flight DDL and the catalog upgrade. Removed 'restore from a snapshot of the schedule' and the universe-key-still-exists wording, which the pages do not state.

Method: documentation only; no commands were run.
