---
id: computing-software.digital-privacy-hygiene.device-hardening.windows-file-history-backups
name: windows-file-history-backups
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, file-history, backups, windows, versioned-backups, external-drive, bitlocker-to-go]
level: intro
status: docs-checked
description: "Set up File History to an external drive or network location, include extra folders in a library, and restore earlier versions of files and folders."
sources:
  - "https://support.microsoft.com/en-us/windows/backup-and-restore-with-file-history-7bf065bf-f1ea-0a78-c1cf-7dcf51cc8bfc"
  - "https://support.microsoft.com/en-us/windows/back-up-your-windows-pc-87a81f8a-78fa-456e-b521-ac0560e32338"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows File History backups

**Goal:** a local, versioned copy of your files for accidental deletion or unwanted changes, using a built-in Windows tool.

## Set up
1. Connect an external drive or have a network location ready.
2. Control Panel > System and Security > **Save backup copies of your files with File History** > **Turn on**.
3. If no drive is chosen, or the wrong one, use **Select drive**; if prompted you can move existing files to the new drive
   or start fresh.

File History backs up all your libraries: Documents, Pictures, Videos and Music, plus custom libraries, and Desktop. To
include another folder, right-click it > Show more options > **Include in library**.

## Restore
1. In File Explorer open the folder that used to hold the file, right-click the folder name > **Restore previous versions**
   (for a top-level folder like C:\, right-click the drive). For library items, right-click where the file is saved, not
   in the library.
2. On the **Previous Versions** tab pick a version (for a file deleted today, choose yesterday's version of the folder).
3. Preview with Open > Open in File History. Restore with **Restore**, or expand Restore > **Restore to...** to avoid
   overwriting the current version.

**Warning:** a plain Restore replaces the current file or folder and the replacement can't be undone. Use Restore to... if
you are unsure.

## Know its limits
Microsoft's page does not cover drive encryption or rotation. Keep a second copy of important files off
the PC, and unplug or rotate the drive so one event cannot affect every copy. Windows Backup (a separate feature) is
described on Microsoft's "Back up your Windows PC" page.

## Verify
- [ ] A test file restored from an earlier version opens correctly.

## Checked
2026-10-28. Confirmed on Microsoft Support (Backup and restore with File History): Control Panel path, Turn on, Select
drive, default libraries and Desktop, Include in library, Previous Versions restore steps and the overwrite warning.
Removed (not on the fetched pages): Advanced settings values, BitLocker To Go advice, Files last copied indicator, the
Restore personal files route, Windows 10 Settings path, and ransomware claims.
Method: documentation only; no commands were run.
