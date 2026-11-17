---
id: computing-software.general-digital-literacy.file-management.resolving-cloud-sync-conflicts
name: resolving-cloud-sync-conflicts
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, cloud-sync, onedrive, google-drive, sync-conflict, sync-errors, conflicted-copy, onedrive-red-x, sync-paused]
level: intro
status: docs-checked
description: "Fix cloud sync problems: Dropbox conflicted copies, merging duplicate versions, and OneDrive files blocked by invalid names."
sources:
  - https://help.dropbox.com/organize/conflicted-copy
  - https://support.microsoft.com/en-us/onedrive/restrictions-and-limitations-in-onedrive-and-sharepoint
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resolving cloud sync conflicts and errors

**Goal:** one correct copy of each file, synced everywhere.

## Conflicts
Dropbox creates a conflicted copy when two people (or two devices) change the same file at once,
when one edits offline while another edits, or when a file is left open on another computer. The
file name gets the editor's username, "conflicted copy" and the save date. Dropbox says the best fix
is to compare both versions and merge them manually, then remove the extra copy.

To avoid them, collaborate in real time (for example Dropbox Paper or Office online), or take
turns: move the file out of the shared folder while you work, or tell collaborators it is in use.

## Names OneDrive will not sync
OneDrive's restrictions page lists characters that are invalid in file and folder names, including
`" * : < > ? / \`, and says leading and trailing spaces are not allowed. Rename the file and sync again.

## Gotchas
- Never "fix" sync by copying the whole folder elsewhere and back; it creates thousands of duplicates.
- Deleting in a synced folder deletes in the cloud.

## Verify
- [ ] No conflicted copies remain and every file syncs.

## Checked
2026-11-01. Confirmed on Dropbox "What's a conflicted copy?": causes, file naming, manual merge, prevention. Confirmed on Microsoft's OneDrive restrictions page: invalid characters and leading/trailing spaces. Removed (no page read): status icon table, OneDrive/Google conflict naming and Keep both/Merge prompts, reset command, error remedies, bin retention days.

Method: documentation only; no commands were run.
