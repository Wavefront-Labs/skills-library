---
id: computing-software.systems-network-administration.immich.system-integrity-checks
name: system-integrity-checks
category: computing-software
field: systems-network-administration
product: immich
tags: [integrity, checksum, untracked-files, missing-files, maintenance]
level: practitioner
status: docs-checked
description: "Read Immich's nightly integrity report: untracked files, missing files and checksum mismatches, what each usually means and how to rerun checks."
sources:
  - https://docs.immich.app/administration/system-integrity
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: interpret the integrity report and act on each finding safely.

Immich runs three checks, all nightly at 3am by default, at an interval you can customise:

- Untracked files: a path exists in Immich's directories but is not in the database.
- Missing files: the database references a path that is not on disk.
- Checksum mismatches: a file's checksum no longer matches the stored one.

The checksum check is the most taxing, so it has extra time and progress limits and may take a couple of days to cover everything.

Results are on the Administration, Maintenance page. There you can trigger a full check of one job or all of them, or a refresh, which only re-examines items already reported and sees whether they are fixed.

Typical causes:

- Untracked: usually partial thumbnails or encoded videos never cleaned up. These are normally safe to delete because they can be regenerated. Run the "missing" jobs for thumbnails and encoded videos from the queues page and watch the server logs.
- Missing: you deleted files from the internal library on disk (unsupported), or the storage has a fault. Investigate carefully.
- Checksum mismatch: often file system corruption, or an earlier manual edit of a library file, which is also unsupported.

Review each item individually. Editing or deleting files in the internal library on disk is not supported; if you edited a file, the supported fix is to delete the mismatched asset from Immich and reupload it as a new asset.

## Checked

2026-11-09. Read the System Integrity page in full and checked every claim against it (three checks, nightly 3am default, checksum limits, maintenance page actions, causes, queues page jobs). Removed the System Settings menu path and the "except to take backups" wording, which the page does not state.

Method: documentation only; no commands were run.
