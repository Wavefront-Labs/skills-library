---
id: computing-software.database-administration.yugabytedb.pitr-snapshot-schedules
name: pitr-snapshot-schedules
category: computing-software
field: database-administration
product: yugabytedb
tags: [pitr, snapshot-schedule, create-snapshot-schedule, retention, timestamp-history-retention-interval-sec, yb-admin, point-in-time-recovery]
level: advanced
status: docs-checked
description: "Enable point-in-time recovery with create_snapshot_schedule, choose interval and retention, and understand history retention flags, limits, and disk effects."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/backup-restore/point-in-time-recovery/enable-pitr.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/reference/configuration/yb-master.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/backup-restore/point-in-time-recovery/rewind.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/troubleshoot/nodes/disk-full.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PITR snapshot schedules

PITR keeps enough history to restore a database to any moment in a retention window.

Create a schedule (interval and retention are in minutes):
```
yb-admin --master_addresses ip1:7100,ip2:7100,ip3:7100 create_snapshot_schedule 1440 4320 ysql.production_db
```
That takes a snapshot daily and keeps three days of history; the command prints the schedule ID as JSON. For YCQL pass the keyspace name (the page's example uses `<keyspace_name>` with no prefix). A schedule is what enables rewind and clone to PIT; inspect at PIT only needs the history retention flags, and restore to PIT works from a specific snapshot. Manage schedules with:
```
yb-admin --master_addresses <masters> list_snapshot_schedules
yb-admin --master_addresses <masters> delete_snapshot_schedule <schedule_id>
```

Rules:
- A database or keyspace can have at most one schedule.
- On universes managed by YugabyteDB Anywhere, manage PITR only from its UI; using yb-admin and the UI together can cause conflicts and yb-admin changes are not reflected in the UI.
- The global `--timestamp_history_retention_interval_sec` (default 900 seconds) applies to every YSQL database and YCQL keyspace whether or not PITR is on. With a schedule, the per-database retention is the maximum of that global value and the schedule's snapshot interval (for example, an 8 hour global value with a 4 hour interval keeps 8 hours of history).
- Deleting a schedule with `delete_snapshot_schedule` disables rewind and clone for that database or keyspace and deletes the schedule's snapshots.
- Retained history uses disk. Per the disk-full troubleshooting page, tables dropped under PITR stay in a HIDDEN state until retention passes, so dropping them does not free space immediately.

Failure mode: point-in-time reads at a time before the retention interval might be refused after a compaction and return a Snapshot too old error, so size retention for how long it takes you to notice mistakes.

## Checked

2026-11-04. Confirmed against the Enable and disable PITR page (create_snapshot_schedule interval and retention in minutes, list and delete, which PITR methods need a schedule, retention is the maximum of the global flag and the schedule interval), the yb-master reference (flag default 900 and the Snapshot too old behaviour) and, for added points, the Rewind page (one schedule per database, Anywhere UI warning) and the disk-full page (HIDDEN tables). Removed: the `ycql.<keyspace>` prefix (the page uses the bare keyspace name), the `timestamp_syscatalog_history_retention_interval_sec` claim (it appears only on the Inspect at PIT page, which says to set it together with the main flag), and 'delete schedules before an in-place upgrade' (no cited page says it). A pre-existing sentence that restoring older than retained history fails with Snapshot too old was narrowed to what the yb-master reference says.

Method: documentation only; no commands were run.
