---
id: computing-software.database-administration.time-series-databases.timescale-extension-upgrade
name: timescale-extension-upgrade
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-migration, timescale-extension-upgrade, timescaledb, postgresql]
level: practitioner
status: docs-checked
description: "Upgrade the timescaledb extension safely."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading the extension

**Goal:** Upgrade the timescaledb extension safely.

## Steps
- Install the new package version and restart PostgreSQL, then in each database run it from a fresh session: `psql -X -d mydb -c "ALTER EXTENSION timescaledb UPDATE;"` (or `UPDATE TO '<version>'`).
- The `-X` flag stops a `.psqlrc` from accidentally triggering a load of the old extension.
- Different databases in one PostgreSQL instance can run different TimescaleDB versions; `ALTER EXTENSION` upgrades each independently.
- You cannot upgrade TimescaleDB and PostgreSQL at the same time: update the extension, upgrade PostgreSQL if your path requires it (`pg_upgrade`; the TimescaleDB version must be the same before and after), then update the extension again if needed.
- Check the version with `\dx timescaledb` (or `SELECT extversion FROM pg_extension WHERE extname = 'timescaledb';`).
- If you use Toolkit, update `timescaledb_toolkit` to 1.6.0 first, then `timescaledb`, per the upgrade planning note.
- Back up first; see the upgrade planning page for the supported path.

**Gotcha:** Running other statements before `ALTER EXTENSION ... UPDATE` can load the old library into the session; use `psql -X` and make the update the first command.

## Verify
- The reported version is the new one.
- Policies still run and continuous aggregates refresh.

## Checked

Checked 2026-11-03 against the timescale/docs repository: self-hosted/upgrades/minor-upgrade, about-upgrades, upgrade-pg, upgrade-docker, downgrade, _partials/_migrate_self_postgres_implement_migration_path. Removed: 'one minor version at a time unless release notes allow skipping' (not stated; follow the compatibility matrix and the plan-your-upgrade-path page) and the 'test on a replica' step.

Method: documentation only; no commands were run.
