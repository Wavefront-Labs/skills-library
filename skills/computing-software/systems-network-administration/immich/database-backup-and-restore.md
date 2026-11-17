---
id: computing-software.systems-network-administration.immich.database-backup-and-restore
name: database-backup-and-restore
category: computing-software
field: systems-network-administration
product: immich
tags: [database-dump, restore, backups, maintenance, sql-gz]
level: practitioner
status: docs-checked
description: "Use Immich's automatic database dumps and the web restore flow: schedule, retention, manual dump, restore from settings or onboarding, uploaded .sql.gz files."
sources:
  - https://docs.immich.app/administration/backup-and-restore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: back up and restore the Immich database through the web UI.

Immich stores file paths and user metadata in the database and does not scan the library folder, so database backups are essential. Dumps contain no photos or videos; keep a copy of the files in `UPLOAD_LOCATION` too.

Automatic dumps go to `UPLOAD_LOCATION/backups`. Schedule and retention live in Administration, Settings, Database Dump Settings (default: daily at 2:00 AM, keep the last 14).

Manual dump: Administration, Job Queues, Create job, "Create Database Dump", Confirm.

Restore on a running instance:

1. Administration, Maintenance, expand "Restore database backup".
2. Choose a backup (version and date are shown) and click Restore, then confirm.

Restore replaces the current database. Immich first creates a restore point, restores, runs migrations if needed, then runs a health check; on failure it rolls back automatically.

Restore on a fresh install: populate `.env` and `docker-compose.yml`, move `backups`, `encoded-video`, `library`, `profile`, `thumbs` and `upload` into the new `UPLOAD_LOCATION`, run `docker compose up -d`, then choose "Restore from backup" on the welcome screen. Immich enters maintenance mode and shows folder integrity checks before you pick a backup.

You can upload a `.sql.gz` file in the restore section; it appears with an `uploaded-` prefix. An indicator shows whether the backup version matches the running version, was created with a different version, or could not be determined. A different version may need migrations.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/backup-and-restore (Database sections).
Removed or reworded: the colour names for the version indicators.
Method: documentation only; no commands were run.
