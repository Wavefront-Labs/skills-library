---
id: computing-software.database-administration.pgbackrest.backup-scheduling-cron
name: backup-scheduling-cron
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, cron, scheduling, backup, diff]
level: practitioner
status: docs-checked
description: "pgBackRest has no internal scheduler; use cron entries such as weekly full and daily diff."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: automate regular backups.

pgBackRest has no scheduler of its own, so run backups from cron or similar. Example: a full backup on Sunday and a differential backup Monday through Saturday, both at 6:30 AM. If the crontab is first installed mid-week, the first differential job runs as a full backup because no full exists.

```
30 06 * * 0   pgbackrest --type=full --stanza=demo backup
30 06 * * 1-6 pgbackrest --type=diff --stanza=demo backup
```

Practical points from the docs:

- With multiple repositories, backups must be scheduled individually per repository using `--repo`. Backup types and retention often differ by repository.
- A successful backup runs `expire` afterward when `expire-auto` is y (the default).
- Set `repo1-retention-full` so it matches the schedule; the number counts full backups, not days, unless `repo1-retention-full-type=time`.

If a backup is stopped by `pgbackrest stop`, it will not start; see the start and stop skill.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (Multiple Repositories). Removed: the claim that the guide gives a cron example, and remarks about repository-host placement and retention that the pages do not state. 

Method: documentation only; no commands were run.
