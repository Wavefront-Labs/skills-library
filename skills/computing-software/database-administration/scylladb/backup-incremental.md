---
id: computing-software.database-administration.scylladb.backup-incremental
name: backup-incremental
category: computing-software
field: database-administration
product: scylladb
tags: [backup, incremental-backups, scylla-yaml, point-in-time, hardlinks]
level: practitioner
status: docs-checked
description: "Incremental backups in ScyllaDB: incremental_backups setting, hard links to the backups directory after each flush, what a point-in-time restore needs, and manual cleanup."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/backup-restore/backup.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Incremental backup

Incremental backup is disabled by default. When enabled, ScyllaDB hard-links each SSTable into a `backups` directory right after it is flushed, capturing the delta since the last snapshot.

Enable it in `/etc/scylla/scylla.yaml`, then restart ScyllaDB:

```
incremental_backups: true
```

From then on flushed SSTables appear in `keyspace_name/table_name-UUID/backups` under the data directory, for example `mykeyspace/team_roster-91cd2060f99d11e6a47a000000000000/backups`.

A complete point-in-time backup requires:
- a snapshot (see the snapshot backup skill);
- all incremental backups and commit logs from the time of the snapshot onward.

ScyllaDB does not delete incremental backups automatically: delete the ones you no longer need (after copying them to external storage).

At restore time, after copying the chosen snapshot back, copy the files from the `backups` folder into the table directory too, and fix ownership with `chown -R scylla:scylla`. Do not rely on incremental backups alone: without the base snapshot they are not a restorable set. Also back up the schema (see the snapshot backup skill): data can only be restored into a recreated table schema.

## Checked

2026-11-04. Confirmed against backup.rst and restore.rst: disabled by default, incremental_backups in scylla.yaml, hard link after flush, directory layout, point-in-time requirements, no automatic deletion, restore copy and chown step. Removed the unsupported hard-link and schema-only wording.

Method: documentation only; no commands were run.
