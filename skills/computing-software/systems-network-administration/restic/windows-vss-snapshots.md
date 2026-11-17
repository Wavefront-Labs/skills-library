---
id: computing-software.systems-network-administration.restic.windows-vss-snapshots
name: windows-vss-snapshots
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, windows, vss, use-fs-snapshot, volume-shadow-copy]
level: advanced
status: docs-checked
description: "Back up open files on Windows with restic --use-fs-snapshot and tune vss.timeout, vss.provider and volume exclusions."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows VSS snapshots

On Windows, `--use-fs-snapshot` creates a VSS snapshot for each volume that holds files to back up and reads files from it, so files locked by another process can be backed up:

```
restic -r /path/to/repo backup --use-fs-snapshot \path\to\data
```

## Options (`-o`)

- `vss.timeout`: how long to wait for the snapshot; default 120 seconds, e.g. `-o vss.timeout=2m30s`.
- `vss.exclude-all-mount-points`: leave mount points out of the shadow copy.
- `vss.exclude-volumes`: volumes to skip when snapshotting.
- `vss.provider`: choose a provider by GUID, by name, or with the alias `MS` for the Microsoft provider.

## Registry exclusions

Files listed under `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\BackupRestore\FilesNotToSnapshot` are excluded from shadow copies by Windows itself, so they may be absent from the backup.

## Related Windows notes

- Cloud placeholder files can be skipped with `--exclude-cloud-files`.
- Restoring symlinks needs `SeCreateSymbolicLinkPrivilege` or administrator rights; restoring full security descriptors needs `SeRestorePrivilege`, `SeSecurityPrivilege` and `SeTakeOwnershipPrivilege`, otherwise only the DACL comes back.

## Checked

Checked 2026-11-08 against the restic Backing up page (040_backup) and Restoring from backup page (050_restore), both read in full. Confirmed: --use-fs-snapshot, vss.timeout default 120 seconds, vss.exclude-all-mount-points, vss.exclude-volumes, vss.provider by GUID or name with the MS alias, the FilesNotToSnapshot registry key, --exclude-cloud-files, and the symlink and security-descriptor privileges. Removed: the elevated-shell requirement for VSS and the antivirus advice, which the pages do not state.

Method: documentation only; no commands were run.
