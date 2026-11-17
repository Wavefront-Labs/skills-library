---
id: computing-software.digital-privacy-hygiene.device-hardening.time-machine-encrypted-backups
name: time-machine-encrypted-backups
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, time-machine, backups, macos, encrypted-backup, nas-backup, apfs-snapshots, migration-assistant, 3-2-1-backup]
level: intro
status: docs-checked
description: "Set up Time Machine on a Mac with an external drive, turn on Encrypt Backup, know the backup schedule, and keep the backup password safe."
sources:
  - "https://support.apple.com/en-us/104984"
  - "https://support.apple.com/guide/mac-help/back-up-files-mh35860/mac"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Time Machine encrypted backups

**Goal:** automatic, versioned Mac backups that you can restore, protected by a backup password.

## Set up (macOS Ventura 13 or later)
1. Connect an external drive. Use one with at least twice the capacity of your Mac's storage, used only for Time Machine.
2. System Settings > General > Time Machine > **Add Backup Disk** > pick the drive > **Set Up Disk**.
3. Your Mac might offer to erase the drive for Time Machine. Erasing deletes everything on it: copy off anything you need first.
4. Turn on **Encrypt Backup** to protect it from unauthorised access and create a backup password. You will need that
   password to restore files, so store it in your password manager.
5. If asked whether to claim existing backups made on another computer, claim them to make them part of this Mac's backups.

## Schedule
Time Machine makes hourly backups for the past 24 hours, daily backups for the past month, and weekly backups for all earlier
months; the oldest backups are deleted when the disk is full. Choose Back Up Now from its menu bar menu for an immediate
backup. To change frequency: Open Time Machine Settings > Options > Back up frequency.

## Good habits
- Eject the drive, or shut down the Mac, before unplugging it; backups resume when you reconnect.
- Apple's Time Machine pages also cover backing up to multiple storage devices and excluding items.

## Restore
Time Machine can restore any or all files to the same Mac or a different Mac; follow Apple's "Restore your Mac from a
backup" article. Test a restore after the first backup.

## Checked
2026-10-28. Confirmed on Apple Support 104984: capacity guidance, dedicated disk, setup path, erase prompt, Encrypt Backup
and backup password, claim-existing-backups prompt, schedule and retention, Back Up Now, frequency option, reconnect and
eject behaviour, restore to same or different Mac. Removed (not on the fetched pages): NAS and SMB advice, two-disk rotation
detail, local snapshot claims, restore click-paths, ransomware notes.
Method: documentation only; no commands were run.
