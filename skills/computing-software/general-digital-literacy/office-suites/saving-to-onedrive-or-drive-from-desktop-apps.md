---
id: computing-software.general-digital-literacy.office-suites.saving-to-onedrive-or-drive-from-desktop-apps
name: saving-to-onedrive-or-drive-from-desktop-apps
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, cloud-documents, save-to-cloud, autosave-onedrive, google-drive-for-desktop, default-save-location]
level: intro
status: docs-checked
description: "Save Office files to OneDrive or SharePoint from the desktop apps, understand AutoSave versus AutoRecover, and use Save a Copy safely."
sources:
  - https://support.microsoft.com/en-us/office/turn-on-autosave-in-microsoft-365-apps-dbd19b49-ff3a-48f5-8294-671e33a6712c
  - https://support.microsoft.com/en-us/office/collab-files/what-is-autosave
  - https://support.microsoft.com/en-us/office/save-a-copy-before-editing-to-prevent-changing-the-original-file-8aeabebe-952e-449b-b931-ae2b7568771b
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Save to the cloud from desktop apps

## Microsoft Office
- The **AutoSave** switch is at the top left of the app. It needs an active Microsoft 365 subscription and a file stored in OneDrive or SharePoint; it does not work with CSV files, older formats (.xls, .ppt, .doc), files embedded in another file, presentations in slide show mode, or while OneDrive sync is paused.
- Local files get **AutoRecover** instead, on by default and saving about every 10 minutes (File > Options > Save).
- Select the file name at the top of the app to see its location and version history.
- With AutoSave on, edits go straight to the original, so use **Save a Copy** before editing when you need to keep the original. For files opened from OneDrive or SharePoint, Save a Copy replaces Save As on the File menu: choose OneDrive as the location and name the copy; later edits will not appear in the original.

## Gotchas
- A file kept in two synced cloud folders can conflict; keep it in one.

## Verify
- [ ] The title bar shows the file is saved to OneDrive or SharePoint and the file appears on the web.

## Checked

2026-10-27. Microsoft Support 'Turn on AutoSave in Microsoft 365 apps', 'What is AutoSave?' and Save a copy pages (read 2026-10-27). Confirmed AutoSave requirements and blockers, AutoRecover interval, Save a Copy behaviour. Removed: Save to Computer by default and default-location option names, Google Drive for desktop drive letter and plug-in retirement, iCloud and Apple notes, Move File steps (not confirmed on current pages). Description and scope narrowed to Microsoft files.

Method: documentation only; no commands were run.
