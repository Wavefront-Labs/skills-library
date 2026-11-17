---
id: computing-software.database-administration.pgbackrest.block-incremental-backup
name: block-incremental-backup
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, block-incremental, repo-block, bundling, space-saving]
level: advanced
status: docs-checked
description: "Store only changed blocks of a file between backups with repo-block, which needs bundling enabled."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shrink diff and incr backups of large files.

Block incremental stores only the parts of a file that changed since the prior backup, rather than the whole file. It also improves delta restore, because individual blocks can be fetched without reading an entire file from the repository.

```
[global]
repo1-block=y
repo1-bundle=y
```

Requirements and behavior:

- `repo-bundle` must be enabled first.
- It works best enabled for all backup types, including full. This makes the full slightly larger, but later diff and incr backups use the block maps from the full to save space.
- Block size depends on file size and age: older and larger files get larger blocks, and a file that is old enough is not backed up with block incremental at all.
- Default `repo-block` is n.

Because bundled files cannot be reused when a backup is resumed, a higher `repo-bundle-limit` means fewer resumable files.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Removed: the version requirements (v2.46, v2.52.1), which the fetched pages do not state. 

Method: documentation only; no commands were run.
