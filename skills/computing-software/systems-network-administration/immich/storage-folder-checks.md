---
id: computing-software.systems-network-administration.immich.storage-folder-checks
name: storage-folder-checks
category: computing-software
field: systems-network-administration
product: immich
tags: [mount-check, immich-file, ignore-mount-check-errors, permissions, volumes]
level: practitioner
status: docs-checked
description: "Fix Immich startup failures from folder checks: the .immich marker files, missing volume mounts, permissions, and IMMICH_IGNORE_MOUNT_CHECK_ERRORS."
sources:
  - https://docs.immich.app/administration/system-integrity
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: diagnose an Immich server that refuses to start because of storage folder checks.

At startup Immich validates that it can read and write the volumes it uses. The folders checked are `upload/`, `library/`, `thumbs/`, `encoded-video/`, `profile/` and `backups/`. In each it:

1. Creates a hidden `.immich` file on first run.
2. Reads the hidden file.
3. Overwrites the hidden file.

If any step fails the server will not start. The checks catch incorrect permissions and missing volume mounts. A typical log shows:

```
Verifying system mount folder checks (enabled=true)
ENOENT: no such file or directory, open 'upload/encoded-video/.immich'
```

That means Immich wrote the marker before but cannot find it now. Causes and fixes:

- Permission error: the file exists but cannot be read. Fix ownership or permissions.
- Volume mount changed: correct the volume mount so it points at the original data.
- Marker deleted by hand: recreate it with `touch .immich` in that folder.
- Backup restored without every folder: restore all folders, or create `.immich` in the missing ones.

The `.immich` files track which mounts Immich uses, so do not create or delete them except in these situations.

Only if you fully understand the cause, the checks can be disabled:

```
IMMICH_IGNORE_MOUNT_CHECK_ERRORS=true
```

The docs warn the checks usually point to a real problem that should be solved instead.

## Checked

2026-11-09. Confirmed against the System Integrity page, Folder checks section: folder list, the three startup operations, failure to start, the log example, the four causes, the marker-file note and the IMMICH_IGNORE_MOUNT_CHECK_ERRORS warning. Removed: the docker-compose.yml file name, which the page does not mention.
Method: documentation only; no commands were run.
