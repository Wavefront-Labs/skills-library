---
id: computing-software.general-digital-literacy.file-management.unlinking-a-computer-from-cloud-sync
name: unlinking-a-computer-from-cloud-sync
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-cloud-storage, unlink-onedrive, stop-sync, sign-out-cloud]
level: intro
status: draft
description: "Unlink OneDrive, sign out of Google Drive for desktop, Dropbox or iCloud on a computer you're giving away or switching accounts on, without deleting cloud files."
sources:
  - https://support.microsoft.com/en-us/onedrive
  - https://support.google.com/drive
  - https://help.dropbox.com/installs/unlink-relink-computer
  - https://support.apple.com/icloud
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Unlink a computer from cloud sync

## OneDrive
1. OneDrive cloud icon (taskbar) > gear > **Settings > Account > Unlink this PC** > *Unlink account*.
2. Files already downloaded stay in the local OneDrive folder; online-only files (cloud icon) become unopenable placeholders.
3. Delete the local folder afterwards if the PC is leaving you; the cloud copy is unaffected once unlinked.

## Google Drive for desktop
- Drive icon > gear > **Preferences** > gear > **Disconnect account**. Mirrored files remain locally; streamed (G:) drive disappears.

## Dropbox
- Dropbox icon > avatar > **Preferences > Account > Unlink This Dropbox**. Or remotely at dropbox.com > Settings > Security > *Devices* > delete (stops sync; *Delete files the next time the computer comes online* option for lost devices).

## iCloud
- Mac: System Settings > [your name] > **Sign Out**; choose whether to keep a copy of iCloud Drive files. Windows: iCloud app > *Sign Out*.

## Remote removal
- OneDrive: account.microsoft.com > Devices; Google: myaccount.google.com > Security > *Your devices* > Sign out.

## Gotchas
- **Never delete the local folder while still linked**: the deletion syncs to the cloud (recoverable from the recycle bin for 30 days, but alarming).
- Unlink before resetting or selling the PC; reset alone doesn't revoke the device token.
- Switching accounts: unlink, then sign in with the new account and choose a new folder location to avoid mixing files.

## Verify
- [ ] Cloud website still shows all files, and the device no longer appears in the account's device list.
