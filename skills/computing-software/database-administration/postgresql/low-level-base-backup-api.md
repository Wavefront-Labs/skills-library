---
id: computing-software.database-administration.postgresql.low-level-base-backup-api
name: low-level-base-backup-api
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-backup-start, pg-backup-stop, base-backup, snapshot-backup, backup-label, continuous-archiving]
level: practitioner
status: docs-checked
description: "Take a PostgreSQL physical backup with pg_backup_start/pg_backup_stop around a storage snapshot or file copy, keeping the session open and saving backup_label."
sources:
  - https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP
  - https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADMIN-BACKUP
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Low-level base backup API (pg_backup_start / pg_backup_stop)

Use when copying files yourself (tar, rsync or a file-system tool) instead of pg_basebackup. The functions are `pg_backup_start` and `pg_backup_stop`; the calling connection must stay open for the whole backup. Not for `pg_dump`/`pg_dumpall`.

## Prerequisites
- WAL archiving working (`archive_mode = on`, `archive_command`/`archive_library` succeeding) — the backup is useless without the WAL generated during it.

## Procedure (the session must stay connected throughout)
```sql
-- session 1, keep it open
SELECT pg_backup_start(label => 'nightly-2026-10-18', fast => true);   -- fast = immediate checkpoint
```
```bash
# shell: copy or snapshot the data directory (and every tablespace)
rsync -a --exclude=pg_wal/* --exclude=postmaster.pid --exclude=postmaster.opts <DATA_DIR>/ <BACKUP_DIR>/
# or: lvcreate --snapshot / zfs snapshot / cloud volume snapshot
```
```sql
-- same session 1
SELECT * FROM pg_backup_stop(wait_for_archive => true);
-- returns lsn, labelfile, spcmapfile
```
Write `labelfile` to `<BACKUP_DIR>/backup_label` and `spcmapfile` (if not empty) to `<BACKUP_DIR>/tablespace_map`, byte for byte without modification (open the file in binary mode if needed). These files are critical to recovery.

If session 1 disconnects before `pg_backup_stop`, the backup is aborted automatically; start again. On a primary `pg_backup_stop` also switches to the next WAL segment; on a standby it cannot, so run `pg_switch_wal()` on the primary, and `archive_mode` must be `always` for `wait_for_archive` to wait. Setting `wait_for_archive => false` is only safe if you monitor that every required WAL segment is archived.

## Consistent snapshots
If the file system can take a frozen snapshot of the volume holding everything (data files and WAL), you can copy the data directory from the snapshot without the API; the server then replays WAL as after a crash, so include the WAL files. If data, WAL or tablespaces live on different file systems and simultaneous snapshots are not possible, the docs suggest a short shutdown or a continuous-archiving base backup (this API) instead.

## Restore
1. Put files back, add `backup_label` (and `tablespace_map`).
2. `recovery.signal` + `restore_command` (and a recovery target if PITR).
3. Start; recovery begins from the checkpoint in backup_label and replays archived WAL past the `pg_backup_stop` LSN before it is consistent.

## Verify
- `pg_backup_stop` with `wait_for_archive => true` returns only when the last needed WAL segment is archived.
- Test-restore regularly. `pg_verifybackup` checks backups taken with pg_basebackup against their `backup_manifest`, so it does not apply to a copy made with this API; verify by starting the restored copy and checking the data.

## Gotchas
- Forgetting `backup_label` (or `tablespace_map`): their presence and contents are critical to the recovery process; without them the restore is not a valid backup.
- Scripts that call start and stop in separate `psql -c` invocations fail: each is a new session.
- The docs say to omit the contents of `pg_wal/`, and say you may also omit `postmaster.pid`, `postmaster.opts`, the contents of `pg_replslot/` (otherwise a standby built from the backup can retain WAL indefinitely), the contents of `pg_dynshmem/`, `pg_notify/`, `pg_serial/`, `pg_snapshots/`, `pg_stat_tmp/` and `pg_subtrans/`, files and directories beginning with `pgsql_tmp`, and `pg_internal.init` files.
- Tablespaces outside the data directory must be included, and symbolic links must be archived as links.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): backup chapter (low-level API procedure: archiving must work, `pg_backup_start(label, fast)`, same connection until `pg_backup_stop(wait_for_archive)`, second and third return fields written to `backup_label` and `tablespace_map` unmodified, standby behaviour and `pg_switch_wal`, `wait_for_archive` caveats, omit lists for `pg_wal` and other directories, consistent-snapshot alternative and its multi-file-system limit), `pg_backup_start` function reference and the pg_verifybackup description. Removed the PG15 rename remark, the `wal_level` line and the silent-corruption wording, which the documentation does not give.
Method: documentation only; no commands were run.
