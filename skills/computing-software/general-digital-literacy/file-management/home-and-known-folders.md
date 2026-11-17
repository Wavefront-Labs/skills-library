---
id: computing-software.general-digital-literacy.file-management.home-and-known-folders
name: home-and-known-folders
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-explorer, known-folders, user-folder, home-folder]
level: intro
status: gated
description: "Understand the user home folder and known folders (Desktop, Documents, Downloads, Pictures) on Windows and Mac, move them to another drive safely, and find them again."
sources:
  - https://support.microsoft.com/en-us/windows/experience/fileexplorer/file-explorer-in-windows
  - https://learn.microsoft.com/en-us/windows/win32/shell/known-folders
  - https://support.apple.com/guide/mac-help/change-finder-settings-on-mac-mchlp2803/mac
  - https://support.apple.com/en-us/109344
  - https://support.microsoft.com/en-us/office/back-up-your-folders-with-onedrive-d61a7930-a6fb-4b95-b28a-6552e77c3057
  - https://support.apple.com/en-us/102650
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Home folders and known folders

## Where they live
- **Windows:** Windows 11 pins Desktop, Documents and the other default folders in Quick access (Home) and the navigation pane instead of listing them under This PC.
- **Mac:** `Shift+Command+H` in the Finder opens your Home folder. Finder > Settings > **Sidebar** controls which standard items show; Settings > General > *New Finder windows show* picks the starting folder.
- Known folders are the standard locations apps and backup tools use by default.

## Move a Windows known folder to another drive
- Right-click the folder > Properties > **Location** tab > Move, then Apply (gated: unconfirmed, source is paywalled or blocked). Microsoft's documentation does not cover this dialog on the pages checked; confirm on your PC and do not drag the folder itself.

## Cloud backup redirects them
- **OneDrive:** Settings > Sync and backup > **Manage backup** lets you back up Desktop, Documents and Pictures (and others). Turning a folder off asks whether to keep the files only in OneDrive or only on the PC.
- **iCloud:** System Settings > your name > iCloud > Drive > **Desktop & Documents Folders**. Turning it off leaves the files in iCloud Drive and creates new empty local folders in your home folder.

## Verify
- [ ] A new file saved from an app lands in the expected Documents location.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "File Explorer in Windows", "Back up your folders with OneDrive"; Apple Mac User Guide "Change Finder settings", keyboard shortcuts, and Apple Support "Add your Desktop and Documents files to iCloud Drive" (macOS 27 / Tahoe 26, 2026). The Windows Location-tab move and the advice not to rename the user folder are gated. Removed unconfirmed claims: AppData and Library paths, Restore Default.
Method: documentation only; no commands were run.
