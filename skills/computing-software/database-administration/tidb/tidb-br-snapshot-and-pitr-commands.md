---
id: computing-software.database-administration.tidb.tidb-br-snapshot-and-pitr-commands
name: tidb-br-snapshot-and-pitr-commands
category: computing-software
field: database-administration
product: tidb
tags: [tidb, br, tiup-br, backup-full, log-start, log-status, restore-point, log-truncate]
level: advanced
status: docs-checked
description: "Run BR log backup tasks, regular full backups, PITR with br restore point, and log truncation using tiup br command examples."
sources: ["https://docs.pingcap.com/tidb/stable/br-pitr-guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb br snapshot and pitr commands

Log backup (a cluster can only run one log backup task at a time):

```shell
tiup br log start --task-name=pitr --pd "${PD_IP}:2379" --storage 's3://backup-101/logbackup?...'
tiup br log status --task-name=pitr --pd "${PD_IP}:2379"
```

Status shows NORMAL, PAUSED or ERROR and `checkpoint[global]`; you can use PITR to restore to a point before the checkpoint. The `end` field currently does not take effect. If you authorize S3 through IAM roles, set `--send-credentials-to-tikv` to false.

Full (snapshot) backup, run on a fixed schedule such as every 2 days:

```shell
tiup br backup full --pd "${PD_IP}:2379" \
  --storage 's3://backup-101/snapshot-${date}?...'
```

PITR:

```shell
tiup br restore point --pd "${PD_IP}:2379" \
  --storage='s3://backup-101/logbackup?...' \
  --full-backup-storage='s3://backup-101/snapshot-${date}?...' \
  --restored-ts '2022-05-15 18:00:00+0800'
```

BR picks the data it needs. Restore runs in a full phase then a log phase; target tables switch to `restore` mode (no reads or writes) and return to `normal` afterward.

Retention: read a snapshot's time point with `tiup br validate decode --field="end-version" --storage ...`, then delete older log backups with `tiup br log truncate --until=${FULL_BACKUP_TS} --storage=...`. PITR needs the full backup before the restore point plus the logs after it, so only truncate logs before a full snapshot you keep. The page gives 600 GB/h for truncation and, per TiKV node, 2 TiB/h for snapshot restore and 30 GiB/h for log restore (test results; actual figures vary).

## Checked

2026-11-04. Confirmed against the TiDB Log Backup and PITR Guide: commands, `--send-credentials-to-tikv`, status values, table restore mode, truncate procedure and speeds. Removed: `--backupts` semantics, `restore db/table`, `--filter` usage and the snapshot-GC error claim, which that page does not cover.
Method: documentation only; no commands were run.
