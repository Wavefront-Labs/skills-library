---
id: computing-software.database-administration.pgbackrest.process-max-parallelism
name: process-max-parallelism
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, process-max, parallel, performance, restore]
level: practitioner
status: docs-checked
description: "Size process-max for backup, restore and archive commands separately."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: parallelise without hurting the database.

`process-max` (default 1, allowed 1 to 999) sets how many processes compress and transfer files. Do not set it so high that it hurts database performance.

Guidance from the user guide:

- Backup: usually no more than 25% of available CPUs. Backups do not need to run fast as long as they run regularly and should not impact the database.
- Restore: can and should use all available CPUs, because the cluster is shut down during restore and generally nothing else important runs. Consider other clusters on the host.
- SFTP repositories transfer slowly, so raise process-max to parallelise; object stores with high latency also benefit.

```
[global]
process-max=3

[global:archive-push]
process-max=2

[global:archive-get]
process-max=2
```

Using command sections keeps the archive values out of backup and restore and lets archive-push and archive-get differ. Test with `--type=full backup` before and after: for very small backups the gain is not obvious, but it grows with database size.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (Parallel Backup / Restore). Removed: the claim about delta restore SHA-1 efficiency. 

Method: documentation only; no commands were run.
