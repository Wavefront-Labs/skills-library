---
id: computing-software.systems-network-administration.backup-and-recovery.restic-restore-and-mount
name: restic-restore-and-mount
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic, restic-restore, restic-mount, restic-dump, fuse, file-restore, backup]
level: practitioner
status: docs-checked
description: "Restore data from restic: full or filtered restores to a target, single files with dump, browsing snapshots via FUSE mount, and permissions and verification details."
sources:
  - https://restic.readthedocs.io/en/stable/050_restore.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# restic restore and FUSE mount

**Goal:** get back exactly the files needed, from the right snapshot, with correct ownership.

## Find the snapshot and file
```bash
restic snapshots --host web01 --path /srv/www
restic ls latest /srv/www/config | head
restic find 'config.php' --host web01
```

## Restore to a target directory
```bash
restic restore latest --host web01 --path /srv/www --target /restore
restic restore 4bba301e --target /restore --include /srv/www/config --exclude '*.log'
```
Restore to a separate location and copy back after checking; restoring in place over live data risks mixing versions. Useful flags: `--verify` (verify restored file contents), `--dry-run`, `--overwrite always|if-changed|if-newer|never` (default always), `--delete` (remove target files absent from the snapshot; preview with `--dry-run -vv`), `--sparse`, and `--ownership-by-name` (restore owners by user and group name; POSIX ACLs are always restored numerically). `snapshotID:subfolder` restores only that subtree.

## Single file to stdout
```bash
restic dump latest /srv/www/config/config.php > /tmp/config.php
restic dump --archive tar latest /srv/www/config > config.tar
```

## Browse with FUSE (Linux, macOS, FreeBSD)
```bash
mkdir /mnt/restic
restic mount /mnt/restic &
ls /mnt/restic/snapshots/          # default layout: ids/<id>, snapshots/<time>, hosts/<host>/<time>, tags/<tag>/<time>
cp /mnt/restic/ids/4bba301e/srv/www/config/config.php /tmp/
umount /mnt/restic                 # or Ctrl-c in the restic mount terminal
```
The mount is read-only. Mounting works only on Linux, macOS and FreeBSD (on Linux the `fuse` module must be loaded and `fusermount` in the PATH); use `restore` or `dump` on Windows. The mountpoint must not overlap the repository directory. `mount` suits a few files; `restore` is significantly faster for many.

## Gotchas
- `restic dump` of a folder produces tar by default (`--archive zip` for zip); `dump latest /` archives the whole snapshot.
- `latest` without `--host`/`--path` picks the latest snapshot across all hosts.

## Verify
Compare restored files with known checksums or open them in the application; for full restores, compare file counts and sizes with the snapshot (`restic stats <id>`).

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: restore flags (--verify, --overwrite modes and default, --delete, --sparse, --ownership-by-name), snapshotID:subfolder syntax, mount platforms and fusermount requirement, default mount path templates, dump archive formats, latest resolution with --host and --path (050_restore, man pages). Removed the unconfirmed egress claim.

Method: documentation only; no commands were run.
