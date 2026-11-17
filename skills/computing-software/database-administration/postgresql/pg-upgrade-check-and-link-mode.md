---
id: computing-software.database-administration.postgresql.pg-upgrade-check-and-link-mode
name: pg-upgrade-check-and-link-mode
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-upgrade, major-version-upgrade, pg-upgrade-check, pg-upgrade-link, pg-upgrade-clone, upgrade-standbys, rsync-standby]
level: advanced
status: verified
description: "Run a PostgreSQL major upgrade with pg_upgrade: --check rehearsal, --link vs --copy vs --clone trade-offs, upgrading streaming standbys with rsync, and the rollback limits."
sources:
  - https://www.postgresql.org/docs/current/pgupgrade.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_upgrade: check and link mode

**Goal:** a major version upgrade of a multi-TB cluster in minutes of downtime,
with a known rollback point.

## Prepare
- Install the new major's server + contrib + every extension build.
- `initdb` the new cluster with the **same** locale/encoding/checksum settings as
  the old (`pg_controldata` shows checksums). A checksum mismatch fails the check (`old cluster does not use data checksums but the new one does`); on a Windows test a different `--locale` or encoding on the new cluster did not fail `--check`, so do not rely on it to catch those.
- Copy relevant config into the new cluster (do not copy postgresql.conf wholesale across majors; diff it).

## Rehearse with --check (old cluster can be running)
```bash
/usr/lib/postgresql/17/bin/pg_upgrade \
  -b /usr/lib/postgresql/15/bin -B /usr/lib/postgresql/17/bin \
  -d /var/lib/postgresql/15/main -D /var/lib/postgresql/17/main \
  -o '-c config_file=/etc/postgresql/15/main/postgresql.conf' \
  -O '-c config_file=/etc/postgresql/17/main/postgresql.conf' \
  --check
```
Fix everything reported: missing extension libraries, `reg*` types in user tables,
incompatible `sql_identifier`, unknown-type columns, prepared transactions, etc.

## Run (both clusters stopped)
| Mode | Speed | Old cluster after |
|---|---|---|
| `--copy` (default) | Copies all files: hours for TB | Intact: rollback = start old |
| `--link` | Hard links: minutes regardless of size | **Unusable once the new cluster starts** |
| `--clone` | Reflink copy (XFS/Btrfs/APFS): fast, independent | Intact |
| `--copy-file-range` (PG17) | Kernel copy offload | Intact |
Add `--jobs=<cores>` to parallelise per database/tablespace.
With `--link`, take a filesystem snapshot or verified backup first: it is your only rollback.

## Standbys
Streaming standbys cannot be pg_upgraded independently. Documented fast path
(with --link): after upgrading the primary and **before** starting it, rsync
from the primary's old+new directories to each standby with
`rsync --archive --delete --hard-links --size-only --no-inc-recursive old new standby:/parent/`
(copies only the new catalog files and recreates hard links), then configure and
start standbys. Otherwise rebuild standbys with pg_basebackup after the upgrade.

## After
- Start the new cluster, run `vacuumdb --all --analyze-in-stages` (statistics are
  not carried over before PG18), update extensions, then delete the old cluster
  with the generated `delete_old_cluster.sh` when sure.
- Replication slots for logical replication are not migrated before PG17.

## Verify
`SELECT version();`, extension versions updated, application smoke tests, and
`pg_upgrade_output.d` logs without errors.

## Checked
- PostgreSQL 17.6 (Windows), old and new clusters created with `initdb`: `--check` works with the old cluster running and ends `*Clusters are compatible*`; a user table with `regproc`/`regprocedure` columns fails with `Checking for reg* data types in user tables` and a `tables_using_reg.txt` list; running the upgrade with the old cluster up is refused (`There seems to be a postmaster servicing the old cluster`); `--link --jobs=2` succeeded and printed the statistics and `delete_old_cluster` instructions; afterwards the old cluster would not start (`global/pg_control` renamed away), the new one had 20,000 rows, `citext` 1.6, no `pg_stats` rows until `vacuumdb --all --analyze-in-stages`; `--clone` and `--copy-file-range` report `not supported on this platform` on Windows (flags exist); the PG17 notes add slot preservation and `copy_file_range`; the standby `rsync` command is quoted from the PG17 pg_upgrade manual (rsync itself not run).
