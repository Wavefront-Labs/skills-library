---
id: computing-software.database-administration.pgbackrest.point-in-time-recovery
name: point-in-time-recovery
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, pitr, recovery-target, target-time, restore]
level: advanced
status: docs-checked
description: "Recover to a time, LSN, xid or named point and choose a backup that ended before it."
sources:
  - https://pgbackrest.org/user-guide.html
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: roll the cluster back to just before a mistake.

PITR plays WAL from a backup up to an lsn, time, transaction id or restore point. Time-based is usually most useful. Take the time from PostgreSQL itself and include the time zone offset to avoid conversions:

```
psql -Atc "select current_timestamp"
pgbackrest --stanza=demo --delta --type=time \
  "--target=2026-10-15 07:08:16.882666+00" --target-action=promote restore
```

PostgreSQL can only play forward. If you restore a backup that was taken after the target (for example `--set` of an incremental that no longer contains the dropped table), recovery fails with `recovery ended before configured recovery target was reached`. Let pgBackRest select a backup that ended before the target; it cannot do that automatically for types `xid` and `name`, where `--set` is needed.

Options: `--target-action` (default `pause`; `promote` or `shutdown`), `--target-exclusive` (stop just before the target; for lsn, time or xid), `--target-timeline`.

pgBackRest writes `restore_command`, `recovery_target_time` and `recovery_target_action` into postgresql.auto.conf. The PostgreSQL log shows where recovery stopped and the last completed transaction.

## Checked

2026-11-08: the PITR example, the failure message when the backup is too new, automatic backup selection and its xid/name exception confirmed in the User Guide; --target-action (default pause), --target-exclusive and --target-timeline confirmed in the Command Reference restore options. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
