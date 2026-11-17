---
id: computing-software.systems-network-administration.incus.export-import-instance-backup
name: export-import-instance-backup
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, export, import, backup, tarball, instance-only]
level: practitioner
status: docs-checked
description: "Back up an Incus instance to a compressed file with incus export (optionally --instance-only) and restore it with incus import, with name-clash behaviour."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_backup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export and import instances

```
incus export <instance> [<file_path>]
incus export <instance> --instance-only
incus import <file_path> [<instance_name>]
```

- Without a path, the file is written to the working directory as `<instance>.<extension>` (for example `my-container.tar.gz`).
- Snapshots are included by default; `--instance-only` leaves them out.
- Store the backup on a different file system for reliability.
- Import uses the original name unless you give one. If an instance of that name exists in the target storage pool, import errors: delete the old one or choose another name.
- Custom storage volumes are not in the export; back them up separately.
- Other approaches: snapshots, or copying the instance to a secondary backup server (see the move-instances how-to).

## Checked

2026-11-04: confirmed against the Incus instance backup how-to (export/import syntax, default file name, snapshots included by default, `--instance-only`, name-clash error, custom volumes excluded). Removed: the `incus copy` command, which the page does not name for backup servers.

Method: documentation only; no commands were run.
