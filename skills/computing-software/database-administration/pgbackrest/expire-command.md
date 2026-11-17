---
id: computing-software.database-administration.pgbackrest.expire-command
name: expire-command
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, expire, retention, dry-run, backup-set]
level: practitioner
status: docs-checked
description: "Run expire manually: scope with --repo or --set, preview with --dry-run, and use --oldest or --archive-expire-before."
sources:
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: remove old backups and WAL on demand.

`expire` runs automatically after each successful backup (`expire-auto`, default y) and can also be run by hand. It applies each configured repository's retention settings; `--repo` restricts it to one repository. Archive retention is checked every time expire runs.

```
pgbackrest --stanza=demo expire
pgbackrest --stanza=demo --dry-run expire
```

Options:

- `--set=<label>` expires that backup and its dependents regardless of retention, but at least one full backup must remain. The docs warn it permanently removes backups and archives not needed for consistency and may negate PITR; when retention options are configured, override them to maximum values for ad hoc expiration to avoid unintended archive expiry.
- `--oldest` expires the oldest full backup set that can be removed (a newer full must remain), as if retention were decremented by one. It cannot be combined with `--set`, and with time-based retention it uses count for that run.
- `--archive-expire-before=<segment>` removes WAL earlier than the given segment, only if not needed by a retained backup. It is intended mainly for archive-only repositories.
- `--checksum-page-error` (default y) stops expire if the oldest retained backup would contain checksum errors.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Command Reference (pgbackrest.org/command.html) and the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Nothing needed removing. 

Method: documentation only; no commands were run.
