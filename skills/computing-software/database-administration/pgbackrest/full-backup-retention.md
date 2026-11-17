---
id: computing-software.database-administration.pgbackrest.full-backup-retention
name: full-backup-retention
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, retention, repo-retention-full, expire, full-backup]
level: practitioner
status: docs-checked
description: "Set repo-retention-full by count or time and understand when the oldest full backup is actually removed."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep the right number of full backups.

`repo-retention-full` is the retention count or time, and `repo-retention-full-type` says which:

- `count` (default): keep that many full backups.
- `time`: keep full backups for that many days.

```
[global]
repo1-retention-full=2
repo1-retention-full-type=count
```

A new backup must complete before expiration happens. With type count and value 2 there are three full backups stored before the oldest is expired. With type time and value 30, a full backup is expired only if another full backup at least 30 days old remains. With count, expiration is not concerned with when backups were created but with how many must be retained.

When a full backup expires, all differential and incremental backups that depend on it expire too. If the option is not defined a warning is issued; for indefinite retention set it to the maximum (allowed range 1 to 9999999). By default archived WAL is retained for the backups that have not expired (see `repo-retention-archive`).

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest Command Reference (pgbackrest.org/command.html) (expire). Removed: the claim about the expire run removing archive after the next full and the out-of-space warning remark; the time example now uses the page's 30 days. 

Method: documentation only; no commands were run.
