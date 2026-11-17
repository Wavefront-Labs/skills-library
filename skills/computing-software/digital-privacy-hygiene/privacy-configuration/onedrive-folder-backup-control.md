---
id: computing-software.digital-privacy-hygiene.privacy-configuration.onedrive-folder-backup-control
name: onedrive-folder-backup-control
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, onedrive-folder-backup, onedrive, windows-privacy, cloud-sync]
level: practitioner
status: draft
description: "Find out whether Windows silently backs up Desktop, Documents and Pictures to OneDrive, turn folder backup off safely, and keep local copies."
sources:
  - "https://support.microsoft.com/onedrive"
  - "https://learn.microsoft.com/en-us/sharepoint/redirect-known-folders"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# OneDrive folder backup and what it uploads

**Goal:** control whether personal files go to Microsoft's cloud, and stop it without losing files.

## What happens
Windows 11 setup (signed in with a Microsoft account) often enables OneDrive **folder backup** (known folder move) for
Desktop, Documents and Pictures. Those folders now live inside the OneDrive folder and sync to the cloud. The free 5 GB
fills quickly, prompting upgrades. Files are encrypted at rest by Microsoft but not end-to-end encrypted.

## Check
OneDrive icon > gear > **Settings** > **Sync and backup** > **Manage back up**: shows which folders are backed up.
File Explorer path `%USERPROFILE%\OneDrive\Desktop` instead of `%USERPROFILE%\Desktop` also means it's on.

## Turn it off safely
1. Make sure all files are **downloaded locally** first: select the folders > right-click > **Always keep on this
   device** (files marked "Available when online" exist only in the cloud).
2. Manage back up > toggle each folder off > Stop backup.
3. Windows offers to leave files in OneDrive; check the local folder afterwards and copy back anything that only
   appears under the OneDrive path.
4. Optionally unlink the PC (Settings > Account > Unlink this PC) or uninstall OneDrive.

## If you keep it
- Use **Personal Vault** for sensitive documents (extra authentication).
- Protect the Microsoft account with strong MFA; anyone with access sees your Desktop.
- Remember sync isn't backup; keep File History or another versioned backup too.

## Gotchas
- Deleting files from the OneDrive folder after turning off backup can delete the cloud copy and vice versa while it's
  still linked; unlink before cleaning up.
