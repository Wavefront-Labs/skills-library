---
id: computing-software.database-administration.pgbackrest.start-fast-and-checkpoint
name: start-fast-and-checkpoint
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, start-fast, checkpoint, backup, pg-backup-start]
level: practitioner
status: docs-checked
description: "start-fast forces an immediate checkpoint at backup start instead of waiting for the next scheduled one."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop backups from idling at the start.

A backup begins with PostgreSQL's backup-start call, which by default waits for the next regular checkpoint. `start-fast` (default `n`) requests an immediate checkpoint instead, so the backup starts at once.

```
[global]
start-fast=y
```

The log confirms the choice: `execute backup start: backup begins after the requested immediate checkpoint completes`. Otherwise the backup starts after the next regular checkpoint.

The option passes `y` to the fast parameter of the PostgreSQL backup start function, which forces the checkpoint.

Related: `archive-check` (default y) checks that all WAL segments required to make the backup consistent are in the archive before the backup completes; leave it on unless another method archives WAL. With backup from standby, the backup is started and stopped on the primary, then the command waits for standby replay to reach the backup start LSN.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html). Removed: the claim that the guide recommends start-fast=y and the busy-cluster advice. 

Method: documentation only; no commands were run.
