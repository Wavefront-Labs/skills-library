---
id: computing-software.database-administration.time-series-databases.influxdb-backup-restore
name: influxdb-backup-restore
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-backup, influxdb-backup-restore, influxdb, flux]
level: practitioner
status: docs-checked
description: "Take and test consistent backups of an InfluxDB 2.x instance."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/backup/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/restore/
  - https://docs.influxdata.com/influxdb/v2/admin/backup-restore/backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InfluxDB backup and restore

**Goal:** Take and test consistent backups of an InfluxDB 2.x instance.

## Steps
- Full backup: `influx backup /backups/influx-$(date +%F) -t $INFLUX_TOKEN` (usage is `influx backup [flags] path`).
- Single bucket: `influx backup /backups/b --bucket sensors`.
- Restore full: `influx restore --full /backups/influx-<date>` (replaces all data and restores key-value data such as tokens, dashboards and users).
- Restore a bucket to a new name: `influx restore /backups/b --bucket sensors --new-bucket sensors_restored`. Restore cannot write into an existing bucket, hence `--new-bucket`.
- Ship backups off host (object storage) and keep several generations.

**Gotcha:** `--full` restores tokens and users to the backup state, so rotated tokens come back. If the backup came from an instance with token hashing (the default from OSS 2.9.0), it holds no plaintext operator token: pass one with `--operator-token` (influx CLI 2.8.0+).

## Verify
- A restore into a scratch instance returns the expected row counts.
- Backup job exit code and file size are monitored.

## Checked

2026-11-03. Confirmed in the `influx backup` and `influx restore` CLI pages and the v2 backup page: usage, `--bucket`, `--full`, `--new-bucket`, `--operator-token`, the no-restore-into-existing-bucket note and the full-restore scope. Removed: the operator-token requirement for backup and the incremental-backup claim (neither stated).
Method: documentation only; no commands were run.

