---
id: computing-software.systems-network-administration.restic.restore-snapshot
name: restore-snapshot
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, restore, include, exclude, target, sparse, xattr]
level: intro
status: docs-checked
description: "Restore a restic snapshot or part of it to a target directory using latest, host and path filters, include and exclude patterns, and sparse files."
sources:
  - https://restic.readthedocs.io/en/stable/050_restore.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring from a snapshot

```
restic -r /srv/restic-repo restore <snapshot-id> --target /path/to/restore
restic -r /srv/restic-repo restore latest --target /path/to/restore --host myhost --path /path/to/data
```

`latest` picks the newest snapshot. With `--host` and `--path`, they only choose the snapshot; `--path` does not limit which files are restored.

## Restoring a subset

- `--include` / `--exclude` limit the restore; they are mutually exclusive.
- `--iinclude` / `--iexclude` ignore case.
- `--include-file`, `--exclude-file` and the `i` variants read patterns from a file.
- `restore <snapshot>:<subfolder>` restores one directory, and patterns are then relative to it.

Find file paths with `restic ls latest` or `restic find <name>`.

## Other options

- `--sparse` writes long runs of zeros as holes. Off by default.
- `--include-xattr` / `--exclude-xattr` choose which extended attributes come back; all are restored by default.

## Windows

Symlink restore needs `SeCreateSymbolicLinkPrivilege` or administrator rights. Full security descriptors need `SeRestorePrivilege`, `SeSecurityPrivilege` and `SeTakeOwnershipPrivilege`; without them only the DACL is restored.

## Checked

2026-11-03. Confirmed in the restic docs page Restoring from backup: `latest` with `--host`/`--path`, `--path` only selecting the snapshot, `--include`/`--exclude` mutually exclusive, the `i` variants and `-file` variants, `<snapshot>:<subfolder>` with relative patterns, `restic ls`/`restic find`, `--sparse` off by default, xattr defaults and options, the Windows privileges and DACL-only note. Removed: the scratch-directory advice (not in the docs).

Method: documentation only; no commands were run.
