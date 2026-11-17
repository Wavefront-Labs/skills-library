---
id: computing-software.database-administration.yugabytedb.snapshot-backup-and-restore
name: snapshot-backup-and-restore
category: computing-software
field: database-administration
product: yugabytedb
tags: [snapshots, backup, restore, create-database-snapshot, yb-admin, hard-links, ysql, ycql]
level: practitioner
status: docs-checked
description: "Take and restore distributed snapshots with yb-admin: per-database YSQL snapshots, list and delete commands, what a restore reverts, and why snapshots never expire."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/backup-restore/snapshot-ysql.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/backup-restore/snapshot-ycql.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-admin.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Snapshot backup and restore

A snapshot is a consistent cut of data across all nodes. YugabyteDB does not copy the data; it creates hard links to the relevant files on the same storage volumes, so backup and restore are nearly instantaneous. More stored snapshots mean more space used; the overhead depends on the workload, so test it.

YSQL snapshots are per database (backing up individual YSQL tables is not supported):
```
yb-admin --master_addresses <ip1:7100,ip2:7100,ip3:7100> create_database_snapshot ysql.<database_name>
yb-admin --master_addresses <masters> list_snapshots
yb-admin --master_addresses <masters> restore_snapshot <snapshot_id>
yb-admin --master_addresses <masters> delete_snapshot <snapshot_id>
```
YCQL uses `create_keyspace_snapshot <keyspace>` for a keyspace with its tables and indexes, or `create_snapshot <keyspace> <table>` for one table with its indexes. Creation commands return immediately but the snapshot may take time to complete, so check `list_snapshots` for state COMPLETE before using it. `restore_snapshot` rolls back in place, changing the existing database in the same cluster.

Properties and limits:
- Snapshots never expire and are retained as long as the cluster exists; delete old ones yourself with `delete_snapshot`.
- For YSQL, the in-cluster restore reverts data changes only, not schema changes: if you snapshot, drop a table, then restore, the table is not restored. The YSQL page names workarounds: store snapshots outside the cluster, or use Rewind to PIT or Restore to PIT (tracking issue 12977). The YCQL page makes no statement about this.
- `list_snapshots` returns all snapshots and restores with their states; snapshot states are CREATING, COMPLETE, DELETING, DELETED or FAILED.
- In-cluster snapshots do not protect against filesystem corruption or hardware failure. For backups outside the cluster, use `export_snapshot` plus a copy of the tablet snapshot directories (for YSQL also a `ysql_dump` schema file and a check that `yb_catalog_version()` did not change), then `import_snapshot` on restore. YugabyteDB Anywhere automates these steps.

To restore to a chosen time within retained history rather than one fixed point, create a snapshot schedule with `create_snapshot_schedule`; this also enables Rewind to PIT and Clone to PIT for that database.

## Checked

2026-11-04. Confirmed against the YSQL and YCQL snapshot pages (hard links, per-database YSQL snapshots, create/list/delete/restore commands, create_snapshot for one table, never-expire, in-place restore, external-storage export and import) and the yb-admin reference (snapshot commands and states). Corrected: the data-only restore limitation is stated on the YSQL page only, so it is scoped to YSQL. Removed: the claim that a snapshot initially uses no extra space (the pages say only that more snapshots need more space) and the encryption-at-rest universe key claim, which neither snapshot page makes.

Method: documentation only; no commands were run.
