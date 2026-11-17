---
id: computing-software.database-administration.pgbackrest.differential-backup-retention
name: differential-backup-retention
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, retention, repo-retention-diff, differential, expire]
level: practitioner
status: docs-checked
description: "Use repo-retention-diff to keep a rolling set of differential backups and see how incrementals expire with them."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: retain a rolling window of recent differential backups.

`repo-retention-diff` is the number of differential backups to keep.

```
[global]
repo1-retention-full=2
repo1-retention-diff=1
```

Rules from the docs:

- When a differential expires, all incremental backups associated with it also expire.
- Incrementals are not expired by retention independently; they expire with their related full or differential backup.
- Full backups count as differentials for the purpose of this count, which slightly reduces the number of differentials that must be retained.
- When the option is not defined, all differentials are kept until the full backups they depend on expire.

Allowed range is 1 to 9999999.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest Command Reference (pgbackrest.org/command.html) (expire). Removed: the worked example and a rationale sentence the pages do not contain. 

Method: documentation only; no commands were run.
