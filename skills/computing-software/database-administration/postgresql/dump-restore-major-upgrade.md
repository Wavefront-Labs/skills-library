---
id: computing-software.database-administration.postgresql.dump-restore-major-upgrade
name: dump-restore-major-upgrade
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, dump-restore-upgrade, pg-dumpall, major-version-upgrade, pg-restore, upgrade-strategy]
level: practitioner
status: docs-checked
description: "Upgrade PostgreSQL across major versions by dump and restore using the newer client binaries, with parallel restore, globals first and validation steps."
sources:
  - https://www.postgresql.org/docs/current/upgrading.html#UPGRADING-VIA-PGDUMPALL
  - https://www.postgresql.org/docs/current/app-pgdump.html
  - https://www.postgresql.org/docs/current/app-pg-dumpall.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading via dump and restore

Simplest and most robust major upgrade path (also crosses architectures, OSes and encodings), at the cost of downtime proportional to data size. Use it for small/medium databases, when pg_upgrade is impossible (changing locale/encoding/provider, page format changes, data checksums), or to defragment everything at once.

## Rule 1: use the NEW version's pg_dump
The docs recommend using `pg_dump` and `pg_dumpall` from the newer version. `pg_dump` can dump from servers older than itself (current releases read back to 9.2) but refuses to dump from a server with a newer major version.
```bash
/usr/lib/postgresql/17/bin/pg_dump --version
```

## Procedure (old 13 on port 5432, new 17 on 5433)
```bash
NEW=/usr/lib/postgresql/17/bin
# 1. stop writes (app down or REVOKE CONNECT / pg_hba reject), then:
$NEW/pg_dumpall -p 5432 --globals-only > globals.sql            # roles, tablespaces
$NEW/psql -p 5433 -f globals.sql postgres
# 2. each database, directory format, parallel
for db in $($NEW/psql -p 5432 -Atc "SELECT datname FROM pg_database WHERE datallowconn AND datname NOT IN ('postgres','template1')"); do
  $NEW/pg_dump -p 5432 -Fd -j 8 -f dump_$db $db
  $NEW/createdb -p 5433 -T template0 $db                        # add -E/-l if changing encoding/locale
  $NEW/pg_restore -p 5433 -j 8 -d $db --exit-on-error dump_$db
done
# 3. rebuild planner statistics (PG18 pg_dump includes statistics unless --no-statistics; --statistics-only dumps only them)
$NEW/vacuumdb -p 5433 --all --analyze-in-stages
```
Pipe variant without intermediate files (single-threaded): `pg_dump -p 5432 db | psql -p 5433 db`.

## Speed-ups for the restore
- The documentation's bulk-load advice, applied temporarily on the new cluster: larger-than-normal `maintenance_work_mem` and `max_wal_size` (also a longer `checkpoint_timeout`); `archive_mode = off`, `wal_level = minimal` and `max_wal_senders = 0` if archiving or replication would otherwise be on; and, only because the whole database can be recreated from the dump, `fsync = off`, `synchronous_commit = off` and `full_page_writes = off`. **Revert all of them and restart before going live**, then take a fresh base backup.
- `pg_restore -j` restores in parallel (custom and directory formats support parallel restoration).

## Validate
- Row counts on key tables old vs new; `pg_restore` exit code 0 and no errors in the log.
- Extensions present at expected versions (`\dx`), ownership and grants (`\dp` samples), sequences' `last_value` vs old.
- Run the app's smoke tests against the new port before switching connections.

## Gotchas
- Large objects are included in pg_dump by default for whole-database dumps; `-n`/`-t` selective dumps omit them unless `-b`.
- The new server needs the extensions' packages installed before the restore, since extensions are recreated with `CREATE EXTENSION`.
- To shorten downtime for large databases use logical replication instead (old -> new), cutting over after catch-up.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): Upgrading Data via pg_dumpall (use the newer version's dump programs; read back to 9.2), pg_dump reference (refuses servers newer than itself; directory format and `-j`; large objects with `-b`; `--statistics-only`, `--no-statistics`), pg_dumpall `--globals-only`, pg_restore `-j` and `--exit-on-error`, and the "Populating a Database" bulk-load advice (`maintenance_work_mem`, `max_wal_size`, `checkpoint_timeout`, `archive_mode`, `wal_level`, `max_wal_senders`, `fsync`, `synchronous_commit`, `full_page_writes`). Removed the specific `2GB` and `50GB` values and the speed claims, which the documentation does not give.
Method: documentation only; no commands were run.
