---
id: computing-software.systems-network-administration.samba.vfs-recycle
name: vfs-recycle
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, vfs-recycle, recycle-bin, recycle, vfs, file-sharing]
level: practitioner
status: docs-checked
description: "Add a recycle bin to a Samba share with vfs_recycle: repository, keeptree, versions, size limits, exclusions, directory modes and defaults."
sources:
  - https://www.samba.org/samba/docs/current/man-html/vfs_recycle.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vfs recycle
```
[share]
    path = /data/share
    vfs objects = recycle
    recycle:repository = .recycle
    recycle:keeptree = yes
    recycle:versions = yes
```
Options:
- `recycle:repository`: default `.recycle`; where deleted files go.
- `recycle:directory_mode`: default `0700`; `recycle:subdir_mode` defaults to the same.
- `recycle:keeptree`: keep the original directory structure.
- `recycle:versions`: keep duplicates, naming newer ones "Copy #x of filename".
- `recycle:touch` / `recycle:touch_mtime`: update access / modification time on move.
- `recycle:minsize` / `recycle:maxsize`: bytes; files smaller than minsize or larger than maxsize are not put into the repository.
- `recycle:exclude`: file patterns deleted normally (wildcards ok).
- `recycle:exclude_dir`: directories whose files are deleted normally.
- `recycle:noversions`: paths without versioning (only useful with `recycle:versions`).

The module is stackable. The page states no default for keeptree, versions or the size limits. The repository is created when the first file is deleted, and users can recover files from it.

## Checked
2026-11-04: example, option list and defaults compared with the vfs_recycle man page. Removed: an AD DC vfs objects line and a repository-growth gotcha the page does not state.
Method: documentation only; no commands were run.
