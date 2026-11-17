---
id: computing-software.systems-network-administration.backup-and-recovery.restic-backup-options-excludes-and-tags
name: restic-backup-options-excludes-and-tags
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic-exclude, restic-backup, restic, backup-exclusions, restic-stdin, file-level-backup]
level: practitioner
status: docs-checked
description: "Run restic backups well: exclude files and patterns, one-file-system, exclude-caches, tags and hosts for retention grouping, files-from lists, dry runs and exit codes."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# restic backup options

```sh
restic backup / \
  --one-file-system \
  --exclude-file=/etc/restic/excludes.txt \
  --exclude-caches \
  --exclude-if-present .nobackup \
  --tag daily --tag "$(hostname -s)" \
  --host web01 \
  --verbose
```

## Excludes
- `--exclude PATTERN` / `--iexclude` (case-insensitive); `--exclude-file` with one pattern per
  line. Patterns use Go `filepath.Match` plus a `**` wildcard that must be a whole path component (`foo/**/bar`, not `foo**`):
  ```
  /proc
  /sys
  /dev
  /run
  /tmp
  /var/tmp
  /var/cache
  **/node_modules
  *.swp
  ```
- `--exclude-caches` skips directories with a `CACHEDIR.TAG` file.
- `--exclude-if-present FILE` lets users opt out folders.
- `--exclude-larger-than 2G` for oversized files.
- `--one-file-system` stops at mount points (avoids backing up NFS mounts, `/proc`); unsupported on Windows.
- Excludes do not apply to paths named explicitly on the command line (`restic backup ~/work.txt` always saves that file); content inside a backed-up directory is filtered.

## Inputs other than paths
- `--files-from list.txt` (one path per line), `--files-from-verbatim` for odd names.
- `--stdin --stdin-filename db.sql` from a pipe:
  `pg_dump app | restic backup --stdin --stdin-filename app.sql --tag pgdump`.
  Prefer `restic backup --stdin-from-command --stdin-filename app.sql -- pg_dump app`: restic checks the command's exit code and cancels the backup (exit 1, no snapshot) if it fails, which a plain pipe hides.

## Hosts, tags and parents
- `forget` groups snapshots by host+paths by default; consistent `--host` (important in
  containers where hostnames change) and stable path lists keep retention correct.
- Tags (`--tag`) allow different retention for e.g. pre-upgrade snapshots.
- restic picks a parent snapshot to skip unchanged files quickly: by default the latest snapshot in the same `--group-by host,paths` group (override with `--parent`, and set the same `--group-by` on `forget`).

## Dry run and exit codes
`restic backup --dry-run -vv /data` shows what would be added. Exit codes: 0 success, 1
fatal (no snapshot), **3 = snapshot created but some source data could not be read** (treat as warning to
investigate, not success). Monitor them.

## Verify
`restic snapshots --host web01 --tag daily` shows daily snapshots; `restic ls latest | head`
contains expected paths and not the excluded ones; restore test of a sample file succeeds.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: exclude options and pattern grammar (040_backup), explicit sources not excluded, --one-file-system, --files-from variants, --stdin-from-command behaviour and exit code 1, parent selection by --group-by host,paths, exit codes 0/1/3 (manual).

Method: documentation only; no commands were run.
