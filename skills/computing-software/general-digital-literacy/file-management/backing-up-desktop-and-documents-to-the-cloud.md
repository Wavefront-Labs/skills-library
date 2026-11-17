---
id: computing-software.general-digital-literacy.file-management.backing-up-desktop-and-documents-to-the-cloud
name: backing-up-desktop-and-documents-to-the-cloud
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-cloud-storage, onedrive-folder-backup, known-folder-move, icloud-desktop-documents]
level: intro
status: docs-checked
description: "Turn on OneDrive folder backup for Desktop, Documents and Pictures or iCloud Desktop and Documents, understand where files now live, and turn it off without losing anything."
sources:
  - https://support.microsoft.com/en-us/office/back-up-your-folders-with-onedrive-d61a7930-a6fb-4b95-b28a-6552e77c3057
  - https://support.apple.com/en-us/109344
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Back up Desktop and Documents to the cloud

## OneDrive (Windows)
- OneDrive cloud icon > Help & Settings > **Settings** > **Sync and backup** > **Manage backup**. Toggle a folder that says Not backed up, then Save changes.
- Files in a backed-up folder sync to OneDrive and are available on your other devices.
- Turning a folder off asks you to **keep the files only in OneDrive** (removing them from the PC) or **only on my PC** (removing them from OneDrive). If the folder has cloud-only files you must first set them to Always keep on this device.
- Open files cannot be moved: save and close them first. Folders over a 260 character path or files over 250 GB cannot be protected. Personal accounts on a domain-joined PC may see "Folder protection is unavailable".

## OneDrive (Mac)
- Needs the standalone sync app (not the Mac App Store version) and Full Disk Access. OneDrive menu bar icon > three dots > Preferences > **Backup** > Manage backup. After you stop, files already backed up stay in OneDrive; a "Where are my files" shortcut leads to them.

## iCloud (Mac)
- System Settings > your name > iCloud > **Drive** > check *Sync this Mac* is on > turn on **Desktop & Documents Folders** > Done.
- Files move into iCloud Drive and count toward your iCloud storage. Deleting a file on one device deletes it on all; recover from Recently Deleted within 30 days.
- Turning it off leaves the files in iCloud Drive and creates new empty local Desktop and Documents folders in your home folder.

## Gotchas
- Sync is not a backup: a deletion propagates to every device.
- Work or school accounts may enforce folder backup by policy.

## Verify
- [ ] A new file saved to Desktop appears online (onedrive.com or iCloud.com).

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Back up your folders with OneDrive" and Apple Support "Add your Desktop and Documents files to iCloud Drive" (published 14 September 2026). Fixed: OneDrive settings route and stop-backup behaviour (Windows lets you choose where files stay). Removed unconfirmed claims: free plan size, OneDrive path names, 30-day OneDrive recycle bin, Optimise Mac Storage.
Method: documentation only; no commands were run.
