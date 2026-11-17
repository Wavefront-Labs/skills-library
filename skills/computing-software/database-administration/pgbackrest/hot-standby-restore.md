---
id: computing-software.database-administration.pgbackrest.hot-standby-restore
name: hot-standby-restore
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, standby, hot-standby, restore, archive-get]
level: advanced
status: docs-checked
description: "Create a standby from a backup with restore --type=standby, replaying WAL from the archive."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build a hot standby that reads WAL from the repository.

A hot standby using the WAL archive allows read-only queries. Configuration mirrors the primary, using the `standby` restore type so the cluster stays in recovery at the end of the WAL stream.

```
[demo]
pg1-path=/path/to/pgdata
[global]
repo1-host=repository
```

Steps from the guide: create the cluster once so PostgreSQL configuration files exist (it is overwritten on restore), run the restore, then set the archive settings in case of promotion:

```
pgbackrest --stanza=demo --delta --type=standby restore
```

```
archive_command = 'pgbackrest --stanza=demo archive-push %p'
archive_mode = on
```

If the standby will be promoted without becoming the primary, use `--archive-mode=off` or `archive_mode=off`.

Because PostgreSQL pulls WAL from the archive, changes appear on the standby only after the segment containing them is pushed. Force it with `pg_switch_wal()` on the primary and wait.

Verify with `check` on the standby: it logs `check repo1 (standby)` and `switch wal not performed because this is a standby`.

## Checked

2026-11-08: the standby restore type, the demo configuration, archive-mode=off advice, the pg_switch_wal() delay and the standby check log lines confirmed in the User Guide Hot Standby section and the Command Reference restore options. Partial reads: the User Guide, Command Reference and Configuration pages are long, so only the sections relevant to this skill were read, not every page end to end.

Method: documentation only; no commands were run.
