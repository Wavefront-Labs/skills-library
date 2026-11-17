---
id: computing-software.database-administration.pgbackrest.restore-recovery-options
name: restore-recovery-options
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, recovery-option, archive-mode, postgresql-auto-conf, restore]
level: advanced
status: docs-checked
description: "Add recovery settings with --recovery-option and control archiving on the restored cluster with --archive-mode."
sources:
  - https://pgbackrest.org/command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tailor generated recovery configuration.

`--recovery-option` (repeatable key/value) sets an option in `postgresql.auto.conf` (PostgreSQL 12 or later) or `recovery.conf` (earlier versions).

```
[demo]
pg1-path=/path/to/pgdata
recovery-option=primary_conninfo=host=db.example.com port=5432 user=replicator
```

Notes:

- `restore_command` is generated automatically and can be overridden, but the docs advise against it because pgBackRest is designed to handle it.
- Recovery target options (`recovery_target_name`, `recovery_target_time`, and so on) are generated from `--type` and `--target`; do not set them with this option.
- Earlier generated settings are kept as comments marked as removed by a later restore.
- Use `--type=preserve` to leave the existing `postgresql.auto.conf` in place.

`--archive-mode` (PostgreSQL 12 or later) is `preserve` (default) or `off`. Use `off` for a cluster that must be promoted for work but is not meant to become the new primary, so it does not push WAL into the repository. Otherwise the repository may be polluted with WAL that makes restores harder.

Because pgBackRest does not start PostgreSQL after writing these files, you can review them before the first start and adjust anything outside the generated recovery targets.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html), the pgBackRest Command Reference (pgbackrest.org/command.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html). Nothing needed removing. 

Method: documentation only; no commands were run.
