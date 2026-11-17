---
id: computing-software.it-support-helpdesk.desktop-support.restoring-deleted-files-on-windows
name: restoring-deleted-files-on-windows
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, backup, data-recovery, file-restore, previous-versions, file-history, recycle-bin, shadow-copies, windows-file-recovery, winfr]
level: intro
status: draft
description: "Get a user's deleted or overwritten file back on Windows: Recycle Bin, Previous Versions/shadow copies on shares, File History, OneDrive, and winfr as a last resort."
sources:
  - "https://support.microsoft.com/en-us/windows/recover-lost-files-on-windows-10-61f5b28a-f5b8-3cc2-0f8e-a63cb4e1d4c4"
  - "https://learn.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service"
  - "https://support.microsoft.com/en-us/windows/file-history-in-windows-5de0e203-ebae-05ab-db85-d5aa0a199255"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# restoring-deleted-files-on-windows

Goal: recover the file from the cheapest source first, and stop the user
writing over it while you look.

## Ask first (two questions save an hour)
1. Where was it saved (local Desktop/Documents, OneDrive, a network share,
   SharePoint/Teams, USB)? Check the app's recent files list for the path.
2. When did they last see it good, and was it deleted or overwritten?

## Sources, in order
1. **Recycle Bin** (local deletes; network share deletes bypass it).
2. **OneDrive / SharePoint**: web recycle bin (93 days, second-stage bin for
   site collection admins) or **Version history** for overwritten files —
   see the OneDrive restore skill.
3. **Previous Versions** on file servers: right-click the folder → Properties
   → Previous Versions (needs shadow copies enabled on the server volume,
   usually twice daily). Open the snapshot, copy the file out — prefer
   "Copy" to "Restore" so you don't overwrite newer edits.
4. **File History** (if configured, to an external/network drive): Control
   Panel → File History → Restore personal files, or right-click → Restore
   previous versions on the local folder.
5. **Backup system** (Veeam, Azure Backup, M365 backup) — raise to the backup
   team with exact path and time window.
6. **Windows File Recovery** (`winfr`, Microsoft Store) on local NTFS — last
   resort; success drops fast once the disk is written to (SSD TRIM makes it
   unlikely):
   ```cmd
   winfr C: E: /regular /n \Users\alice\Documents\Budget*.xlsx
   ```
   (recover to a different drive).

## Office specifics
- Unsaved/crashed documents: File → Info → Manage Document → Recover
  Unsaved; AutoRecover location `%APPDATA%\Microsoft\Word` (Excel/PowerPoint
  similar).
- Files on OneDrive/SharePoint with AutoSave keep full version history.

## Gotchas
- Restoring a whole folder from a snapshot overwrites other people's newer
  changes on shares — restore to an alternate location and copy back.
- Don't install recovery tools onto the drive you're recovering from.
- Encrypted (EFS) or BitLocker'd drives need the keys for file-carving tools.

## Verify
User opens the restored file and confirms it's the right version; record
source and timestamp in the ticket (useful for backup/retention reviews).
