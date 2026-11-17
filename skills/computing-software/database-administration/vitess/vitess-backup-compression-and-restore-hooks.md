---
id: computing-software.database-administration.vitess.vitess-backup-compression-and-restore-hooks
name: vitess-backup-compression-and-restore-hooks
category: computing-software
field: database-administration
product: vitess
tags: [backup, compression, zstd, external-compressor, hooks, restore, manifest]
level: advanced
status: docs-checked
description: "Choose Vitess backup compression engines, plug in an external compressor and migrate off it safely, and use the vttablet_restore_done hook with its environment variables."
sources:
  - https://vitess.io/docs/25.0/user-guides/operating-vitess/backup-and-restore/overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default vttablet backups use `pargzip`, which writes gzip-compatible files. Built-in compression engines: `pargzip` (default), `pgzip`, `lz4`, `zstd`; built-in decompression: `pgzip`, `lz4`, `zstd`. Select with `--compression-engine-name`. The chosen engine is recorded in the backup MANIFEST and read at restore, so changing the flag later does not break restores of older backups.

External compression runs a separate process that gets the stream on STDIN and writes to STDOUT, which lets you set scheduling priority or pin CPU cores. Flags: `--external-compressor` (the command), `--external-compressor-extension` (only for the xtrabackup engine, the saved file extension), `--compression-engine-name` (a compatible built-in name, or `external`), and `--external-decompressor`. If the engine name is absent or `external`, restores only work when `--external-decompressor` is passed.

Moving from an external compressor to a built-in engine: if the engine is on the supported list, correct `--compression-engine-name` and drop `--external-compressor`. For an unsupported one, first switch the engine name and remove the compressor, and only after the first new backup completes remove `--external-decompressor`; restoring older backups still needs that flag.

Hooks are executables in `${VTROOT}/vthook/` on the tablet. `vttablet_restore_done` runs when a restore finishes, success or failure, with these variables: `TM_RESTORE_DATA_START_TS`, `TM_RESTORE_DATA_STOP_TS` (RFC3339 UTC), `TM_RESTORE_DATA_DURATION`, `TM_RESTORE_DATA_BACKUP_ENGINE` (unset when restoring from a MySQL clone), and `TM_RESTORE_DATA_ERROR` (only on failure).

## Checked

2026-11-04. Compression engines, external flags, the migration procedure and hook variables confirmed in the Backup and Restore Overview page (compression and Hooks sections).

Method: documentation only; no commands were run.
