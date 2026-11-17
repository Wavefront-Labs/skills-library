---
id: computing-software.general-digital-literacy.file-management.path-too-long-and-illegal-file-names
name: path-too-long-and-illegal-file-names
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-operations, file-name-rules, path-too-long, invalid-characters]
level: intro
status: docs-checked
description: "Fix path too long and invalid character problems with the naming rules Windows and OneDrive enforce, including the 260 character path limit."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file
  - https://support.microsoft.com/en-us/office/restrictions-and-limitations-in-onedrive-and-sharepoint-64883a5d-228e-48f5-b3d2-eb39e07630fa
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Path too long and illegal file name characters

## The rules
- **Windows** reserved characters: `<` `>` `:` `"` `/` `\` `|` `?` `*` (and control characters). Reserved names: CON, PRN, AUX, NUL, COM1 to COM9 and LPT1 to LPT9 (also with an extension, such as NUL.txt). A name must not end with a space or a period.
- **Path length:** MAX_PATH is 260 characters. Later Windows versions need a registry key or Group Policy change to remove the limit, and apps must opt in; shorter paths are the reliable fix.
- **OneDrive and SharePoint** do not allow `" * : < > ? / \ |`, leading or trailing spaces, or the names .lock, CON, PRN, AUX, NUL, COM0 to COM9, LPT0 to LPT9, _vti_, desktop.ini, or any name starting with `~$`.
- OneDrive for Mac has supported invalid characters since 28 January 2025; names with such characters still cannot sync on Windows.

## Fixes
1. Shorten folder names near the top of the tree, or move the folder nearer the drive root.
2. Rename offending files: replace reserved characters with `-`.
3. In OneDrive, rename each file the sync app lists as unable to sync (select the item and press `F2` on Windows or `Return` on a Mac).
4. For unzipping failures, extract to a short folder first.

## Verify
- [ ] The copy or sync completes with no skipped files.

## Checked
Date: 2026-10-27. Documentation: Microsoft Learn "Naming Files, Paths, and Namespaces" and Microsoft Support "Restrictions and limitations in OneDrive and SharePoint" (2026). Fixed a stale claim: OneDrive for Mac now supports invalid characters. Removed unconfirmed claims: the 400 character OneDrive limit, Mac Finder forbidding only colon, FAT and exFAT behaviour, the LongPathsEnabled name and File Explorer behaviour.
Method: documentation only; no commands were run.
