---
id: computing-software.database-administration.pgbackrest.restore-type-values
name: restore-type-values
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, restore, recovery-type, standby, immediate]
level: practitioner
status: docs-checked
description: "What each restore --type value does, including preserve, standby and none."
sources:
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the right recovery type.

`--type` values:

- `default`: recover to the end of the archive stream.
- `immediate`: recover only until the database becomes consistent.
- `lsn`: recover to the LSN in `--target` (PostgreSQL 10 or later).
- `name`: recover to the restore point in `--target`.
- `xid`: recover to the transaction id in `--target`.
- `time`: recover to the time in `--target`.
- `preserve`: keep the existing `postgresql.auto.conf` or `recovery.conf`.
- `standby`: add `standby_mode=on` (or the equivalent) so the cluster starts as a standby.
- `none`: write no recovery file; PostgreSQL reaches consistency from WAL present in pg_wal. Provide the WAL or use `archive-copy` at backup.

Warning: avoid `none`. The timeline is not incremented at the end of recovery, which can lead to PostgreSQL archiving duplicate WAL (rejected) and filling the disk, and tools like pg_rewind may misbehave or corrupt. The default type for offline backups is `none` because PITR is impossible with `wal_level=minimal`; an explicitly set type is honored if `wal_level` is above minimal.

```
pgbackrest --stanza=demo --delta --type=standby restore
```

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Command Reference (pgbackrest.org/command.html) (restore --type). Nothing needed removing. 

Method: documentation only; no commands were run.
