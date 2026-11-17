---
id: computing-software.database-administration.pgbackrest.archive-retention-options
name: archive-retention-options
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, retention, repo-retention-archive, wal-archive, pitr]
level: advanced
status: docs-checked
description: "Tune WAL retention separately from backup retention and know what it costs in PITR range."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expire archived WAL more aggressively without breaking restores.

By default WAL is kept for backups that have not expired: archive is expired with full backups according to `repo-retention-full`. Two options change that:

- `repo-retention-archive`: number of backups worth of continuous WAL to retain (1 to 9999999).
- `repo-retention-archive-type`: `full` (default), `diff` or `incr`, meaning which backup types are counted.

```
pgbackrest --stanza=demo --log-level-console=detail \
  --repo1-retention-archive-type=diff --repo1-retention-archive=1 expire
```

Behavior:

- WAL required to make a backup consistent is always retained until that backup expires, whatever you set.
- Full backups count as differentials for diff archive retention.
- `repo-retention-archive` must be set when the type is `incr`.
- If unset with count-based full retention, it defaults to the retention-full (or diff) value so WAL expires only for already expired backups.

Aggressive settings remove the ability to do PITR from backups whose WAL is gone, so the docs do not recommend it and advise leaving the type at the default. Use `--dry-run` with expire to preview what would be removed.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest Command Reference (pgbackrest.org/command.html) (dry-run). Nothing needed removing. 

Method: documentation only; no commands were run.
