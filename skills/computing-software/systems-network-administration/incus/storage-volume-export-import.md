---
id: computing-software.systems-network-administration.incus.storage-volume-export-import
name: storage-volume-export-import
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, storage-volume, export, import, backup, optimized-storage, compression, volume-only]
level: practitioner
status: docs-checked
description: "Back up custom Incus volumes to a file with storage volume export (--compression, --optimized-storage, --volume-only) and restore with import."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/storage_backup_volume.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export and import volumes

```
incus storage volume export <pool> <volume> [<file_path>]
incus storage volume import <pool> <file_path> [<volume_name>]
```

- Default output is `backup.tar.gz` in the working directory; an existing file is overwritten without warning. Store it on another file system.
- `--compression`: gzip by default; name another algorithm (e.g. bzip2) or `--compression=none`.
- `--optimized-storage` (`btrfs` and `zfs` pools): stores a driver-specific blob. Faster, snapshots become differences so they are smaller, but import works only into pools of the same driver.
- `--volume-only` excludes snapshots (included by default).
- Import keeps the original name unless one is given; a name clash in the pool is an error.

## Checked

2026-11-04: confirmed against the Incus custom volume backup how-to (export/import syntax, default `backup.tar.gz`, overwrite warning, `--compression`, `--optimized-storage`, `--volume-only`, import naming). Nothing removed.

Method: documentation only; no commands were run.
