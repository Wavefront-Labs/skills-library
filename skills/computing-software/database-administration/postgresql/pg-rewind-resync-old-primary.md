---
id: computing-software.database-administration.postgresql.pg-rewind-resync-old-primary
name: pg-rewind-resync-old-primary
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, streaming-replication, hot-standby, pg-rewind, wal-log-hints, timeline-divergence, failback, rejoin-standby]
level: advanced
status: docs-checked
description: "Re-attach a failed PostgreSQL primary as a standby with pg_rewind instead of a full re-copy, including prerequisites (wal_log_hints or checksums) and failure cases."
sources:
  - https://www.postgresql.org/docs/current/app-pgrewind.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pg_rewind

**Goal:** after a failover, turn the old primary into a standby of the new one in
minutes by copying only blocks that changed since the timelines diverged.

## Prerequisite (set before you need it)
The target server must have `wal_log_hints = on` **or** data checksums enabled (set it on every node before you need it; docs: pg_rewind requires one of them). Also keep `full_page_writes = on` (default).

## Procedure
1. The old primary (target) must be **shut down cleanly**. If it was not, pg_rewind by
   default starts it in single-user mode to complete crash recovery first;
   `--no-ensure-shutdown` skips that and errors out instead.
2. Run as the postgres OS user on the old primary:
   ```bash
   pg_rewind --target-pgdata=<datadir> \
     --source-server='host=newprimary user=postgres dbname=postgres' \
     --progress --write-recovery-conf
   ```
   `--write-recovery-conf` (`-R`) creates `standby.signal` and appends connection
   settings to `postgresql.auto.conf`; it requires `--source-server`.
   `--dry-run` first to see what it would do. `--restore-target-wal` (`-c`)
   fetches WAL that is no longer in the target's `pg_wal` using the target's `restore_command`.
3. Check `primary_conninfo` / `primary_slot_name`, create the slot on the new
   primary if used, then start the server. It replays from the divergence point.

## When it fails
- pg_rewind expects WAL in the target's `pg_wal` reaching back to the point of divergence. If the target ran for a long time afterwards and that WAL is gone, copy it from the archive or use `--restore-target-wal`; otherwise re-clone with `pg_basebackup`.
- With `--source-server` the source must be running and reachable with a superuser or a role granted EXECUTE on `pg_ls_dir(text, boolean, boolean)`, `pg_stat_file(text, boolean)` and `pg_read_binary_file(text)` (the docs show the grants).
- Files other than changed relation blocks, including configuration files, are copied in full from the source: re-check `postgresql.auto.conf`
  and anything host-specific after the run.
- If some WAL was no longer on the source when pg_rewind ran, make it available at startup with `recovery.signal` and a suitable `restore_command`.

## Gotchas
- Transactions committed on the old primary after divergence are discarded;
  extract them first if they matter (from WAL with pg_waldump or logs).

## Verify
On the new primary, `pg_stat_replication` shows the rejoined node `streaming`;
on the node, `pg_is_in_recovery()` is true and lag drops to zero.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): pg_rewind reference (description: timeline divergence, WAL needed back to the divergence point, `-c/--restore-target-wal`, archive recovery on restart with `recovery.signal` and `restore_command`; prerequisite of `wal_log_hints` or data checksums; target cleanly shut down with single-user crash recovery by default and `--no-ensure-shutdown`; `-R`, `-n`, `-P` options; whole-file copy of non-relation files; the non-superuser role grants). Corrected: pg_rewind itself runs crash recovery for a not-cleanly-stopped target, so the manual single-user step is unnecessary. Removed the quoted error messages, the PG13 version gate and the Patroni remark, which the documentation does not give.
Method: documentation only; no commands were run.
