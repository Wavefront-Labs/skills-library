---
id: computing-software.systems-network-administration.syncthing.temporary-files-and-reserved-names
name: temporary-files-and-reserved-names
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, temporary-files, syncthing-tmp, keeptemporariesh]
level: practitioner
status: docs-checked
description: "Know how Syncthing writes temporary .syncthing.*.tmp files, how long failed ones are kept, and which prefixes are reserved."
sources: ["https://docs.syncthing.net/users/syncing.html", "https://docs.syncthing.net/users/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temporary files

## Safe writes
Syncthing never writes straight to the destination file. Changes are assembled in a temporary copy, then moved over the old version. If a transfer fails, for example because a block is unavailable, the temporary file is kept for up to a day so already-fetched data is not requested again.

`options.keepTemporariesH` controls the retention period in hours (24 in the default configuration).

## Names
- Unix-like systems: `.syncthing.original-filename.ext.tmp`
- Windows: `~syncthing~original-filename.ext.tmp`
- If that would be too long, the name uses a SHA-256 hash of the original filename instead: `.syncthing.<hash>.tmp`, or `~syncthing~<hash>.tmp` on Windows.

Temporary files are normally hidden.

## Reserved prefixes
The prefixes `.syncthing.` and `~syncthing~` belong to Syncthing's namespace. Any file whose name starts with them is automatically ignored and never synchronised. Avoid using them for real data.

## Where it matters
- On Windows, an external versioning script can detect a modification by checking whether a `~syncthing~<name>.tmp` file exists next to the target (the docs' PowerShell recycle-bin example does this).

## Checked

2026-11-09. Confirmed against the Syncthing Understanding Synchronization page (users/syncing) and the Configuration page (users/config, options.keepTemporariesH, default 24), raw rst from syncthing/docs: write-to-temporary-copy behaviour, one-day retention, temp file names including the hash form, hidden files, reserved prefixes. Removed: the claim that leftover temp files are "reused or cleaned up" (the pages only say they avoid re-requesting data); scoped the external-script tip to the Windows example it comes from.

Method: documentation only; no commands were run.
