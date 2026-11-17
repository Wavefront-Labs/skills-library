---
id: computing-software.database-administration.influxdb.back-up-with-influx-backup
name: back-up-with-influx-backup
category: computing-software
field: database-administration
product: influxdb
tags: [backup, influx-backup, operator-token, token-hashing]
level: practitioner
status: docs-checked
description: "Take a full OSS backup with influx backup and a root token, and handle the 2.9.0+ hashed-token caveat by capturing the operator token before upgrading."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/backup-restore/backup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```sh
influx backup path/to/backup_$(date '+%Y-%m-%d_%H-%M') -t <root-token>
```

The command takes the destination directory and the root authorization token (the token created for the first user during setup). It copies all data and metadata into a set of files in that directory.

Limits and caveats from the page:
- Not compatible with InfluxDB versions before 2.0.0; use the 1.x to 2.x upgrade guides to migrate from 1.x.
- It cannot back up InfluxDB Cloud.
- From InfluxDB 2.9.0, with default settings, tokens are hashed, so a backup does not contain a plaintext operator token. To fully restore it you must supply the operator token at restore time with `influx restore --operator-token` (influx-cli v2.8.0+). Capture the operator token you will use for restores before the first 2.9.0 startup.

## Checked

- Date: 2026-11-04
- Confirmed against: https://docs.influxdata.com/influxdb/v2/admin/backup-restore/backup/
- Scope: backup syntax, version caveats and hashed-token note.
- Removed: the closing advice on timestamped directory names.
Method: documentation only; no commands were run.
