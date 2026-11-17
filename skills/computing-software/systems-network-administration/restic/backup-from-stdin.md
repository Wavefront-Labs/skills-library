---
id: computing-software.systems-network-administration.restic.backup-from-stdin
name: backup-from-stdin
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, stdin, stdin-from-command, database-dump, backup]
level: practitioner
status: docs-checked
description: "Back up command output such as a database dump with --stdin-from-command and --stdin-filename instead of piping into --stdin."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backing up data from a command

Use `--stdin-from-command` to let restic run the command and read its output:

```
restic -r /srv/restic-repo backup --stdin-from-command -- mysqldump [...]
```

Everything after `--` is the command and its arguments.

## Why prefer it to a pipe

Piping into `restic backup --stdin` works, but the docs discourage it. With `--stdin-from-command`, restic sees the command's exit status: a non-zero exit cancels the backup, restic exits with code 1 and no snapshot is created. A plain pipe masks the dump's failure and can store an empty backup; if you must use `--stdin`, set `set -o pipefail` and check the pipe's exit code.

## File name

The stream is stored as one file named `stdin` unless you set `--stdin-filename`:

```
restic backup --stdin-from-command --stdin-filename mydb.sql -- mysqldump mydb
```

Restore it later with `restic dump latest mydb.sql > mydb.sql` (see the mount-and-dump skill).

## Checked

Checked 2026-11-08 against the restic Backing up page (040_backup) and Restoring from backup page (050_restore), both read in full. Confirmed: --stdin-from-command with -- before the command, default file name stdin, --stdin-filename, non-zero command exit cancels the backup with exit code 1 and no snapshot, the --stdin warning about masked errors and the pipefail advice, and restic dump latest FILE. Removed: the notes about change detection and deduplication cost, which the pages do not state.

Method: documentation only; no commands were run.
