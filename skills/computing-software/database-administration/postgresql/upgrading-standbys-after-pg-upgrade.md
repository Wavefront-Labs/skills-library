---
id: computing-software.database-administration.postgresql.upgrading-standbys-after-pg-upgrade
name: upgrading-standbys-after-pg-upgrade
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, pg-upgrade, major-version-upgrade, upgrade-standby-rsync, streaming-replication, hard-links]
level: advanced
status: docs-checked
description: "Upgrade streaming standbys alongside a pg_upgrade --link primary using the documented rsync --hard-links procedure, or rebuild them, without a full re-copy."
sources:
  - https://www.postgresql.org/docs/current/pgupgrade.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading streaming standbys after pg_upgrade

Physical standbys cannot replicate across major versions. After `pg_upgrade` on the primary
you either rebuild each standby with `pg_basebackup` (simple, slow for big clusters) or use the
documented **rsync** step, which is for link mode (`--link`) only.

## Preconditions
- Primary upgraded with `pg_upgrade --link`; the directory structure under the old and new
  data directories on the standby must match the primary.
- New PostgreSQL binaries (and the same extension shared object files as the new primary) installed on the standbys;
  the new standby data directories do not exist or are empty. Do not run pg_upgrade on standbys.
- Standbys were running while the old primary shut down, so they received all changes. Before upgrading run
  `pg_controldata` on the old primary and standby: the `Latest checkpoint location` values must match.
  `wal_level` must not be `minimal` on the new primary.
- Save any standby config you need (`postgresql.conf`, `postgresql.auto.conf`, `pg_hba.conf`): the rsync overwrites or removes them.

## Procedure (from the pg_upgrade docs, step "Upgrade streaming replication and log-shipping standby servers")
1. Shut down the old primary (standbys running so they catch up), stop the standbys, then run `pg_upgrade --link` on the primary.
   **Do not start any server yet.**
2. On the primary, for each standby, from the directory **above** the old and new data dirs:
   ```bash
   cd /var/lib/postgresql
   rsync --archive --delete --hard-links --size-only --no-inc-recursive \
     16/main 17/main standby1:/var/lib/postgresql
   ```
   Add `--dry-run` to preview. Tablespaces need a similar rsync per tablespace directory; if `pg_wal`
   is outside the data directories, rsync those too.
3. Configure the standbys for log shipping/streaming. You do not need `pg_backup_start()`/`pg_backup_stop()` or a
   file system backup, since the standbys are still synchronized. Restore `pg_hba.conf` and adjust
   `postgresql.conf` / `postgresql.auto.conf` to match the old cluster.
4. Start the new primary, then the rsync'ed standbys.

## Gotchas
- Use this procedure only after link mode. If you did not use link mode, do not want rsync, or want
  something simpler, recreate the standbys once the new primary is running (for example with `pg_basebackup`).
- Slots: if the old primary is before 17, no slots are copied to the new standby; from 17, only logical
  slots are copied. Recreate the other slots on the standby manually.
- Keep the old cluster until the standbys are verified. After `--link`, starting the new cluster
  means the old one must not be started (the docs list reverting options per mode).

## Verify
On the primary, `pg_stat_replication` shows each standby `streaming` on the new version;
on standbys `SELECT version(), pg_is_in_recovery();` and a test row replicates.

## Checked

2026-10-31. Confirmed against the PostgreSQL pg_upgrade page: the standby section (link mode only, rsync flags, tablespaces, pg_wal, matching directory structure, empty new standby directories, same extension files, save config files, dry-run, no backup needed, slot copying before and from 17.0, start new primary then standbys), the pg_controldata Latest checkpoint location check, standbys running during shutdown, and wal_level not minimal. Removed unconfirmed: `--clone` eligibility, timing claims, the `--size-only` rationale, `primary_slot_name` and `standby.signal` specifics.

Method: documentation only; no commands were run.
