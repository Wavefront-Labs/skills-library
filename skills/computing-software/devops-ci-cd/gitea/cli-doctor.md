---
id: computing-software.devops-ci-cd.gitea.cli-doctor
name: cli-doctor
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-doctor-check, gitea, doctor-recreate-table, doctor-convert, manager-flush-queues, manager-processes, gitea-manager]
level: advanced
status: docs-checked
description: "Diagnose and repair a Gitea instance: doctor check/--fix/recreate-table/convert, migrate, and manager shutdown, restart, flush-queues, logging, processes."
sources: ["https://docs.gitea.com/administration/command-line/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# gitea doctor, migrate and manager

## doctor check
`gitea doctor check` runs a default set of checks. `--list` lists all checks, `--default` runs the defaults, `--all` runs every check, `--run name1,name2` runs named ones. `--fix` repairs what it can; `--log-file=...` adds logging.

## doctor recreate-table
After migrations, old columns/defaults can linger and produce warnings like `Table user Column keep_activity_private db default is , struct default is 0`. Recreate and copy data with correct defaults:
```bash
gitea doctor recreate-table user          # one table
gitea doctor recreate-table table1 table2 # several
gitea doctor recreate-table               # all tables
```
Back up the database first (the docs say highly recommended).

## doctor convert
Converts a MySQL database from utf8 to utf8mb4, or MSSQL from varchar to nvarchar.

## migrate
`gitea migrate` migrates the database; idempotent, and usable to run before the first server start.

## manager (talks to the running server)
- `gitea manager shutdown` graceful stop; `restart` graceful restart (not implemented on Windows).
- `gitea manager flush-queues [--timeout 1m0s] [--non-blocking]`.
- `gitea manager logging pause|resume|release-and-reopen|remove NAME [-g group]|add console|file|conn|smtp`. `release-and-reopen` equals sending SIGUSR1 (reopen log files after rotation). `pause` raises the level to INFO temporarily and Gitea buffers logs only up to a point, then drops them. `add file` takes `--filename/-f`, `--rotate/-r`, `--max-size/-s`, `--daily/-d`, `--max-days/-D`, `--compress/-z`; all adders take `--level/-l`, `--name/-n`, `--group/-g`, `--expression/-e`, `--prefix/-p`, `--flags/-F`, `--stacktrace-level/-L`, `--color`.
- `gitea manager processes [--flat] [--no-system] [--stacktraces] [--json] [--cancel PID]` lists running processes and goroutines; cancel works only on non-system processes.

## Checked

2026-11-03: read https://docs.gitea.com/administration/command-line/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
