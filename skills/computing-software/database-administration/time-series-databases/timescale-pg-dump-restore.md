---
id: computing-software.database-administration.time-series-databases.timescale-pg-dump-restore
name: timescale-pg-dump-restore
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-backup, timescale-pg-dump-restore, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Dump and restore a Timescale database correctly with the extension's pre and post restore steps."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_dump and restore

**Goal:** Dump and restore a Timescale database correctly with the extension's pre and post restore steps.

## Steps
- Dump (works for compressed hypertables without decompressing): `pg_dump -d "$SOURCE" -Fc -f mydb.bak`. Keep track of the PostgreSQL and TimescaleDB versions you dump from.
- On the target, create the database and enable the extension: `CREATE DATABASE newdb;`, `\c newdb`, `CREATE EXTENSION IF NOT EXISTS timescaledb;`.
- Prepare: `SELECT timescaledb_pre_restore();` sets the `timescaledb.restoring` GUC to on and stops background workers.
- Restore: `pg_restore -Fc -d newdb mydb.bak`. Do not use `-j`; the docs say it does not restore the TimescaleDB catalogs correctly.
- Finish: `SELECT timescaledb_post_restore();` resets the GUC and restarts the background workers. You must run it before using the database normally.
- Individual hypertables: `pg_dump --table` omits the information TimescaleDB needs, so dump the schema (`pg_dump -s -d $SOURCE --table <table> > schema.sql`), export data with `\COPY (SELECT * FROM <table>) TO <table>.csv CSV`, restore the schema, run `create_hypertable`, then `\COPY ... FROM` (or `timescaledb-parallel-copy`).

**Gotcha:** Skipping `timescaledb_pre_restore()` leaves the background workers running during the restore; skipping `timescaledb_post_restore()` leaves them stopped.

## Verify
- `SELECT * FROM timescaledb_information.hypertables;` matches the source.
- Row counts per chunk range agree.

## Checked

Checked 2026-11-03 against the timescale/docs repository: self-hosted/backup-and-restore/logical-backup, api/administration (timescaledb_pre_restore, timescaledb_post_restore). Removed: the 'corrupt catalog state' consequence, and the advice to prefer physical backups for large hypertables (not stated there). Added: the `-j` restriction.

Method: documentation only; no commands were run.
