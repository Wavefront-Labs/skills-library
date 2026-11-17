---
id: computing-software.systems-network-administration.restic.file-change-detection
name: file-change-detection
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, change-detection, parent-snapshot, ignore-ctime, ignore-inode, group-by]
level: advanced
status: docs-checked
description: "Understand how restic decides a file is unchanged using a parent snapshot, and when to use --parent, --force, --ignore-ctime and --ignore-inode."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File change detection

Scanning the entire content of a file already backed up is expensive, so restic uses a metadata rule to decide a
file is likely unchanged since the parent snapshot; if so it is not scanned again. Metadata changes (permissions,
ownership and so on) are always included in the backup.

## Choosing the parent

- By default restic groups snapshots by hostname and backup paths and selects the latest snapshot in the group that
  matches the current backup. `--group-by` changes this and defaults to `host,paths`; `paths` selects the latest with
  the same paths regardless of hostname, `host,tags` considers hostname and tags.
- `--parent <snapshot>` specifies a parent manually.
- Normally set `--group-by` on `forget` to the same value.
- Change detection applies only to regular files with exactly the same path as in a previous backup of the same
  location. A renamed file or renamed containing directory is a different file and is scanned again, as is any file
  when you switch between absolute and relative source paths.

## Metadata used (Unix, including Linux and Mac)

For a file at the same location, these must match for its content to be presumed unchanged: mtime, ctime, size and
inode number. Both mtime and ctime are required because Unix programs can freely change mtime. Flags:

- `--force`: turn off change detection and rescan all files.
- `--ignore-ctime`: require mtime to match, but allow ctime to differ.
- `--ignore-inode`: require mtime to match, but allow inode number and ctime to differ. It exists for FUSE-based
  filesystems and pCloud, which do not assign stable inodes.

The device id of the containing mount point is never taken into account; to force a re-scan after e.g. a ZFS snapshot
change, change the mountpoint. On Windows a file is unchanged when path, size and modification time match, and only
`--force` has any effect.

## Practical advice

- Keep hostname and path arguments stable between runs.
- If backups unexpectedly re-read everything, compare `restic snapshots` output for host and paths before changing flags.

## Checked
Compared with the "Backing up" page, section "File change detection": parent selection, `--group-by` default,
`--parent`, the Unix attribute list, `--force`, `--ignore-ctime`, `--ignore-inode` and its reason, mount-point device
note and the Windows behaviour. Removed: the `RESTIC_IGNORE_CTIME` and `RESTIC_IGNORE_INODE` variables, the
statement that a hostname change means no parent is found, and the claim that `--force` ignores the parent
(the page says it turns off change detection).
Method: docs-only read of cited pages, 2026-11-08
