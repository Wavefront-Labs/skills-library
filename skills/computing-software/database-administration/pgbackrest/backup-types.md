---
id: computing-software.database-administration.pgbackrest.backup-types
name: backup-types
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, backup, full, differential, incremental]
level: intro
status: docs-checked
description: "Choose between full, diff and incr backups and know when pgBackRest upgrades the type for you."
sources:
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right backup type.

The `type` option of `backup` takes `full`, `diff` or `incr` (default `incr`).

- full: copies every file; independent of other backups.
- diff: copies files changed since the last full backup.
- incr: copies files changed since the last backup of any type.

```
pgbackrest --stanza=demo --type=full backup
pgbackrest --stanza=demo --type=diff backup
```

Automatic changes: if no prior backup exists, an incr or diff request becomes full, and the log warns `no prior backup exists, incr backup has been changed to full`. After a major PostgreSQL upgrade a requested incr or diff also becomes full.

Restoring an incr needs its chain: the info output shows a `backup reference total` summarising the additional backups required; add `--set` to display the complete reference list. Expiring a full removes the diff and incr backups that depend on it.

Backups run online by default (`online=y`). `--no-online` skips the backup start/stop functions for an offline backup: PostgreSQL must be shut down and pgBackRest errors if it is not. `--force` runs a backup even if pgBackRest thinks PostgreSQL is running; use it with extreme care.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Command Reference (pgbackrest.org/command.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html). Removed: the 'backup reference list' label (the page says 'backup reference total'), the stanza-upgrade claim and the guide-attributed cron schedule; the --no-online/--force sentence was rewritten from the command reference. 

Method: documentation only; no commands were run.
