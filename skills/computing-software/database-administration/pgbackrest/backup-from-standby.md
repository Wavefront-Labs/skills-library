---
id: computing-software.database-administration.pgbackrest.backup-from-standby
name: backup-from-standby
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, backup-standby, standby, repository-host, load-reduction]
level: advanced
status: docs-checked
description: "Offload file copying to a standby with backup-standby while the primary still starts and stops the backup."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reduce primary load during backups.

Requirements: both primary and standby configured (as `pg1-` and `pg2-` on the repository host, in any order; pgBackRest determines which is primary) and `backup-standby` enabled.

```
[demo]
pg1-host=pg-primary
pg1-path=/path/to/pgdata
pg2-host=pg-standby
pg2-path=/path/to/pgdata
[global]
backup-standby=y
```

`backup-standby` values: `y` (standby required), `prefer` (use a standby if available, otherwise the primary) and `n`. With several standbys, the first running one found is used.

How it works: the vast majority of files are copied from the standby and a few from the primary, and the log shows files from each host. The command waits for replay on the standby to reach the backup start LSN.

During a major upgrade the guide disables `backup-standby` until the standby is restored again.

If no standby is running with `backup-standby=y`, the backup cannot proceed because a standby is required; use `prefer` to fall back to the primary automatically.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (Backup from a Standby). Removed: the claim that only non-replicated files such as logs and statistics come from the primary and that the result is identical to a primary backup. 

Method: documentation only; no commands were run.
