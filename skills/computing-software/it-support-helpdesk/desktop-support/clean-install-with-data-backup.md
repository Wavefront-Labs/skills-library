---
id: computing-software.it-support-helpdesk.desktop-support.clean-install-with-data-backup
name: clean-install-with-data-backup
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, clean-install, windows-installation, data-backup, bitlocker-key, licence-check, reinstall-checklist]
level: practitioner
status: draft
description: "Do a clean Windows reinstall without losing anything: pre-flight checklist (data, keys, licences, BitLocker, drivers), the install itself, and the post-install handback."
sources:
  - "https://support.microsoft.com/en-us/windows/reinstall-windows-d8369486-3e33-7d9c-dccc-859e2b022fc7"
  - "https://learn.microsoft.com/en-us/windows/deployment/windows-10-media"
  - "https://support.microsoft.com/en-us/windows/find-your-bitlocker-recovery-key-6b71ad27-0b89-ea08-f143-056f5ab347d6"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# clean-install-with-data-backup

A clean install (wipe and reinstall) fixes deep corruption and malware, but every lost
file or forgotten licence becomes a complaint. Most of the job is the checklist.

## Before: capture
1. **Data**: Is OneDrive Known Folder Move complete (green ticks, no sync errors)? Check
   folders outside KFM: `%USERPROFILE%` root, `C:` root folders users created, Downloads,
   browser data, Sticky Notes, app data the user cares about (e.g. `%APPDATA%\Mozilla`).
   Copy to a network share or external disk with robocopy and verify counts.
2. **Outlook**: local PST files (`Get-ChildItem -Path $env:USERPROFILE -Recurse -Filter *.pst`);
   signatures (`%APPDATA%\Microsoft\Signatures`).
3. **Browser**: confirm the profile is signed in and synced (Edge/Chrome), or export
   bookmarks and passwords per policy.
4. **Licences**: list installed software (`winget list` or Settings > Apps); note products
   with per-device activation (Adobe, CAD, specialist tools) and **deactivate** them first.
5. **Hardware/drivers**: model and serial; download the vendor driver pack or ensure the
   device will get drivers from Windows Update/Intune.
6. **BitLocker**: recovery key escrowed (Entra/AD/MBAM). Not strictly needed for a wipe,
   but if the install fails halfway you'll want it.
7. **Wi-Fi/VPN, printers, mapped drives**: note what the user uses.
8. **Windows activation**: digital licence tied to hardware (reinstall same edition) or
   volume licensing/KMS.
9. Ticket note with everything captured and where it is.

## Install
- Corporate: Autopilot Reset/Wipe or reimage via task sequence instead of manual media.
- Manual: Media Creation Tool USB or corporate ISO; boot from USB (F12/F9/Esc boot menu);
  delete all partitions on the OS disk; install to unallocated space; same edition as the
  licence.

## After: hand back
1. Windows Update until no updates remain; vendor drivers; Device Manager clean (no yellow
   bangs).
2. Enroll/join (Autopilot or manual), apps via Company Portal/standard build, re-activate
   licensed apps.
3. Restore data; user signs into OneDrive and browser; verify Outlook mailbox and PSTs.
4. Walk through with the user: printers, drives, the apps they use daily.
5. Keep the backup for 2 weeks before deleting.

## Gotchas
- "It's all on OneDrive" is often wrong: Desktop not in KFM, files pending upload.
- Wiping a disk with personal data of another user (shared PC) needs both users' backups.
- Deleting the recovery partition removes vendor recovery tools; usually fine for
  corporate devices.

## Verify
User confirms files, email, apps and printers work; Device Manager and Windows Update are
clean; the device shows compliant in management.
