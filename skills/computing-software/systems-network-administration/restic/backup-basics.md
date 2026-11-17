---
id: computing-software.systems-network-administration.restic.backup-basics
name: backup-basics
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, backup, snapshot, one-file-system, verbose, paths]
level: intro
status: docs-checked
description: "Run restic backup on directories and files, read the verbose output, stay on one filesystem, and use --with-atime and --no-scan deliberately."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backing up with restic

```
restic -r /srv/restic-repo --verbose backup ~/work
restic -r /srv/restic-repo backup ~/work.txt
```

Each run creates a snapshot. `--verbose` repeated, or `--verbose=2`, adds per-file detail.

## Useful flags

- `--one-file-system` does not cross filesystem boundaries when backing up `/`; pass extra mounts explicitly, e.g. `backup --one-file-system / /media/usb`.
- `--with-atime` stores access times (they are not saved by default).
- `--no-scan` skips the initial scan that counts files for progress, saving extra I/O at the cost of progress estimates.
- `--tag` labels the snapshot.

## Absolute and relative paths

The paths you pass are recorded in the snapshot, so the same relative path from different working directories makes different snapshot paths. Prefer absolute paths in scripts so snapshots group consistently.

## Check what you made

```
restic -r /srv/restic-repo check
restic -r /srv/restic-repo ls <snapshot-id>
```

`restic help backup` lists every option. For scheduled runs use the exit codes in the backup-exit-codes skill, and run backups from cron or systemd timers, since restic has no scheduler of its own.

## Checked

Checked 2026-11-08 against the restic Backing up page (040_backup), read in full. Confirmed: --verbose and --verbose=2 detail, --one-file-system with extra mounts, --with-atime (atime not saved by default), --no-scan, --tag, absolute versus relative snapshot paths, no built-in scheduler, restic check and ls. Nothing removed.

Method: documentation only; no commands were run.
