---
id: computing-software.database-administration.pgbackrest.backup-resume-and-manifest
name: backup-resume-and-manifest
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, resume, manifest, backup, manifest-save-threshold]
level: advanced
status: docs-checked
description: "How resume reuses files from a failed backup and how often the manifest is saved so resume works efficiently."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand recovery of failed backups.

The `resume` option (default `y`) allows a backup to resume after a previous backup of the same type failed. The docs say this can greatly reduce backup time, but it adds complexity, so it may be disabled in environments that do not need it.

`manifest-save-threshold` (default 1GiB) defines how often the manifest is saved during a backup. Saving matters because the manifest stores the checksums that let resume work efficiently. The actual threshold used is 1% of the backup size or manifest-save-threshold, whichever is greater.

```
[global]
resume=y
manifest-save-threshold=1GiB
```

Bundling interacts with resume. Bundled files cannot be reused when a backup is resumed, so `repo-bundle-limit` (default 2MiB) controls which files can be resumed: files larger than the limit are stored separately and stay resumable, so higher values result in fewer resumable files.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html). Removed: unconfirmed remarks about SHA-1 delta comparison and a guide statement on resume. 

Method: documentation only; no commands were run.
