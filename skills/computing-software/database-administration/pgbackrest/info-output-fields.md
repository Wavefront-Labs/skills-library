---
id: computing-software.database-administration.pgbackrest.info-output-fields
name: info-output-fields
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, info, backup-labels, wal-range, backup-size]
level: practitioner
status: docs-checked
description: "Decode each field in info output: labels, timestamps, WAL range, database and repository sizes, references."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read an info report correctly.

Fields in the text output:

- Labels: backups are listed oldest to newest. The oldest is always full (label ends in `F`); the newest can be full, differential (`D`) or incremental (`I`).
- `wal archive min/max`: lowest and highest WAL in the archive. Gaps may exist because of archive retention or other reasons.
- `timestamp start/stop`: when the backup ran. The stop time identifies which backup to use for point-in-time recovery.
- `wal start/stop`: the WAL range required to make the database consistent on restore. The backup command ensures this range is in the archive before completing.
- `database size`: full uncompressed size of the database. `database backup size`: data actually backed up (equal for full backups).
- `repoN: backup set size`: all files of this backup plus referenced backups needed to restore it. `backup size`: only this backup's files. Sizes reflect compression.
- `backup reference total`: additional backups needed to restore this one. Use `--set` for the full list.
- `cipher`: the repository cipher type; the guide's example shows `none`.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Command Reference (pgbackrest.org/command.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html). Removed: the 'database list' field claim, and the cipher values beyond the guide's example. 

Method: documentation only; no commands were run.
