---
id: computing-software.database-administration.pgbackrest.archive-command-setup
name: archive-command-setup
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, archive-push, archive-command, wal-archiving, postgresql-conf]
level: practitioner
status: docs-checked
description: "Configure PostgreSQL archive_command to call archive-push and the restore_command counterpart."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ship every WAL segment to the repository.

In postgresql.conf:

```
archive_command = 'pgbackrest --stanza=demo archive-push %p'
archive_mode = on
```

`%p` is the WAL segment path supplied by PostgreSQL. If WAL cannot be pushed to any repository, PostgreSQL will not remove it from pg_wal.

Restore adds the reverse automatically. The generated postgresql.auto.conf contains:

```
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

where `%f` is the segment name PostgreSQL needs and `%p` is where to place it.

Relevant options:

- `archive-mode-check` (default y) disallows `archive_mode=always`, because WAL pushed from a standby can have different checksums than the same WAL from the primary.
- `archive-timeout` (default 1m, range 100ms to 1d) is the maximum wait for each WAL segment to reach the repository; it applies to check and backup.
- `archive-missing-retry` (default y) retries a segment that archive-get previously reported missing in async mode; disabling it lets PostgreSQL recognise the end of archived WAL and switch to streaming.
- `archive-async` (default n) moves pushing to a background process.

With several repositories, archive-push writes the WAL to all of them. If WAL cannot be pushed anywhere, PostgreSQL will not remove it from pg_wal and the volume may fill.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html). Nothing needed removing. 

Method: documentation only; no commands were run.
