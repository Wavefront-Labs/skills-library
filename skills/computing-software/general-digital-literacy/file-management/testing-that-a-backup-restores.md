---
id: computing-software.general-digital-literacy.file-management.testing-that-a-backup-restores
name: testing-that-a-backup-restores
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-backup, test-restore, backup-verification, restore-drill, 3-2-1-backup]
level: intro
status: draft
description: "Prove a backup actually works by restoring sample files and a full folder from File History, Time Machine, cloud backup or a phone backup, on a schedule."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
  - https://www.cisa.gov/secure-our-world
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online/always-back-up-your-most-important-data
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test that a backup restores

**Goal:** know, before disaster, that you can get files back.

## Why
Backups fail silently: the drive was unplugged for months, the wrong folders were selected, the password was forgotten, the cloud plan lapsed. Only a restore proves a backup.

## Quick test (every month or two)
1. Pick three files: one old, one changed this week, one photo.
2. Restore each to a **different location** (Desktop › "restore-test"), never over the original.
   - **Windows Backup / File History:** Control Panel › File History › *Restore personal files* (or right-click a file › Properties › *Previous versions*). Windows Backup app restores on a new PC sign-in.
   - **Time Machine (Mac):** open the folder in Finder › menu bar Time Machine icon › *Browse Time Machine Backups* › choose a date › **Restore** (hold Option to restore to a different place via right-click › *Restore to…*).
   - **OneDrive / Google Drive / iCloud:** web › *Recycle bin* or file **Version history**; check today's edits exist in the cloud.
   - **External drive copy:** open the file directly from the drive.
3. Open each restored file; check it isn't empty or corrupt and the date is recent.

## Full drill (yearly)
- Restore a whole folder or do a phone restore to a spare device; time how long it takes.
- Confirm you can still find backup passwords/encryption keys without the original computer.
- Check the **3-2-1** rule: 3 copies, 2 different media, 1 off-site (cloud or another house).

## Gotchas
- Sync is not backup: deleting or ransomware-encrypting a synced file propagates; check that version history or a separate backup exists.
- Encrypted backups without the key are worthless; store the key in a password manager.

## Verify
- [ ] Restored files open correctly; last backup date is within your target (e.g. 24 hours).
