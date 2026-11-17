---
id: computing-software.general-digital-literacy.file-management.full-system-image-backup
name: full-system-image-backup
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-backup, system-image, disk-image, macrium-reflect, time-machine]
level: intro
status: draft
description: "Make a full disk image of a Windows PC with a third-party imaging tool or the legacy System Image tool, use Time Machine on a Mac, and test bare-metal restore."
sources:
  - https://support.microsoft.com/en-us/windows/back-up-your-windows-pc-87a81f8a-78fa-456e-b521-ac0560e32338
  - https://support.apple.com/en-us/104984
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Full system image backup

File backups save documents; an **image** saves the whole drive (Windows, apps, settings) so a dead disk can be replaced and restored in one go.

## Windows
- **Legacy tool:** Control Panel › *Backup and Restore (Windows 7)* › **Create a system image** › external drive. Still present in Windows 10/11 but deprecated and unmaintained; fine for a one-off.
- **Better:** a dedicated imaging app with scheduling and incremental images (Macrium Reflect, Veeam Agent Free, the drive maker's tool such as Acronis True Image for WD/Crucial/Samsung editions).
- Always create the app's **rescue USB** (WinPE) as you set up; without it you cannot restore onto a blank drive.
- Windows Backup (the Settings app) is **not** an image: it saves files, settings and app list to OneDrive.

## Mac
- **Time Machine** (System Settings › General › Time Machine › Add Backup Disk) is the restore-everything tool: on a new or wiped Mac, Migration Assistant or macOS Recovery › *Restore from Time Machine*.
- Bootable clones (Carbon Copy Cloner, SuperDuper!) are optional on Apple silicon; not needed by most people.

## Restore test
- Boot the rescue USB once and confirm it sees the backup drive. Restore a single file from the image (most tools mount images as a drive letter).

## Gotchas
- BitLocker: keep the recovery key; an image restored onto new hardware may ask for it.
- Images are large; keep 2 generations and delete older ones.

## Verify
- [ ] Rescue media boots and lists your latest image; a file restored from it opens.
