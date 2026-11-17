---
id: computing-software.general-digital-literacy.file-management.show-file-extensions-and-hidden-files
name: show-file-extensions-and-hidden-files
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-explorer, finder, show-file-extensions, hidden-files, file-name-extensions, dotfiles, appdata, library-folder]
level: intro
status: docs-checked
description: "Turn on file name extensions and show hidden files in Windows File Explorer and macOS Finder, and know which hidden folders are safe to look in."
sources:
  - https://support.microsoft.com/en-us/windows/experience/fileexplorer/file-explorer-in-windows
  - https://support.apple.com/guide/mac-help/change-finder-settings-on-mac-mchlp2803/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Show file extensions and hidden files

**Goal:** see what a file really is.

## File extensions
- **Windows 11:** File Explorer > **View** > **Show** > **File name extensions**.
- **macOS:** Finder > Settings > Advanced > **Show all filename extensions** (shows extensions even for files with Hide extension selected).
- Why: `invoice.pdf.exe` appears as `invoice.pdf` with extensions hidden; with them on you see it is a program.

## Hidden files
- **Windows 11:** File Explorer > **View** > **Show** > **Hidden items**.

## Gotchas
- Renaming a file to a new extension does not convert it.
- Do not delete or move items in hidden system or app-data folders unless following specific instructions.

## Verify
- [ ] Files in Downloads show `.pdf`, `.docx`, `.zip` and so on after their names.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "File Explorer in Windows" (View > Show > File name extensions, Hidden items); Apple Mac User Guide "Change Finder settings on Mac" (Advanced > Show all filename extensions; macOS 27 / Tahoe 26, 2026). Removed unconfirmed claims: Windows 10 menu, AppData path, the macOS hidden-files key combination and Library route, warning text.
Method: documentation only; no commands were run.
