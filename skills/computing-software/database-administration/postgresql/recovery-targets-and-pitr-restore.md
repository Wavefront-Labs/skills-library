---
id: computing-software.database-administration.postgresql.recovery-targets-and-pitr-restore
name: recovery-targets-and-pitr-restore
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, continuous-archiving, recovery-target-time, recovery-signal, restore-command, point-in-time-recovery, pitr, recovery-target-action, timeline]
level: advanced
status: docs-checked
description: "Restore a PostgreSQL base backup to a precise moment with restore_command, recovery.signal and recovery_target_* settings, then promote onto a new timeline."
sources:
  - https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-PITR-RECOVERY
  - https://www.postgresql.org/docs/current/runtime-config-wal.html#RUNTIME-CONFIG-WAL-RECOVERY-TARGET
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PITR: recovery targets

**Goal:** bring the cluster back to "just before the bad `DELETE` at 14:03:12"
using a base backup plus archived WAL.

## Procedure (PG12+, no recovery.conf)
1. Stop the damaged server if running; move its data dir aside (keep `pg_wal`
   contents: unarchived WAL may be needed).
2. Restore the base backup taken **before** the target time into the data dir, and remove old files from `pg_wal/`.
3. Copy (not move) any unarchived WAL segments saved from the old `pg_wal` into the new one.
4. In postgresql.conf (or postgresql.auto.conf):
   ```conf
   restore_command = 'cp /archive/%f %p'
   recovery_target_time = '2026-10-16 14:03:00+00'
   recovery_target_inclusive = false
   recovery_target_action = 'pause'
   ```
5. Create an empty `recovery.signal` file in the data directory and start the server. Consider restricting
   `pg_hba.conf` until you are sure the recovery succeeded.
6. It replays WAL and pauses at the target. Connect (`hot_standby` must be on) and check
   the data is there and the bad change is not.
7. Happy: `SELECT pg_wal_replay_resume();` ends recovery. Too early: shut down, set a later target,
   restart to continue. Too late: restore the base backup again.

## Target choices
| Setting | Use |
|---|---|
| `recovery_target_time` | Wall-clock time; always include a time zone |
| `recovery_target_xid` | Stop at a specific transaction id (ids are assigned at start, but transactions can complete in a different order) |
| `recovery_target_lsn` | Exact WAL location (`pg_lsn`) |
| `recovery_target_name` | A named point created earlier with `pg_create_restore_point('before_migration')` |
| `recovery_target = 'immediate'` | Stop as soon as a consistent state is reached (the end of the backup) |

At most one of `recovery_target`, `recovery_target_lsn`, `recovery_target_name`, `recovery_target_time`, `recovery_target_xid`
may be set (it is an error otherwise); they take effect only at server start. `recovery_target_inclusive` (default on) controls
whether the target itself is included.

## Gotchas
- `recovery_target_action` defaults to `pause`; if `hot_standby` is not enabled, pause
  acts like `shutdown`. `promote` ends recovery and accepts connections at once. With `shutdown`,
  `recovery.signal` is not removed, so the next start shuts down again until you remove it.
- `recovery_target_timeline` defaults to `latest`; `current` follows the timeline of the base backup. You
  rarely set it except in re-recovery situations. `restore_command` is also asked for `.history` files and must
  return nonzero for files that are not in the archive.
- `recovery_target_time` needs a numeric UTC offset or a full time zone name, not an abbreviation.
- Restoring in place over production destroys the evidence; restore to a separate
  host and copy the needed rows back when only some data is wrong.

## Verify
After recovery ends, the server removes `recovery.signal` and `SELECT pg_is_in_recovery();` returns false.

## Checked

2026-10-31. Confirmed against the PostgreSQL continuous archiving (PITR recovery steps) and recovery target configuration pages: recovery.signal, the five target settings and the one-target rule, `recovery_target_inclusive`, `recovery_target_timeline` default, `recovery_target_action` values and pause behaviour, pg_wal_replay_resume, time zone format, restore_command rules. Removed unconfirmed: pgbackrest example, pg_waldump tips, timeline file naming, the commit-timestamp bullet, log message text, the `latest`-since-PG12 claim.

Method: documentation only; no commands were run.
