---
id: computing-software.general-digital-literacy.file-management.copying-a-file-path
name: copying-a-file-path
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-explorer, copy-file-path, path-bar, full-path]
level: intro
status: gated
description: "Show the Finder path bar and copy a folder path, jump to a typed path in File Explorer or Go to Folder; the Windows Copy as path command is flagged unconfirmed."
sources:
  - https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
  - https://support.apple.com/guide/mac-help/get-file-folder-and-disk-information-on-mac-mchlp1774/mac
  - https://support.apple.com/en-us/102650
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Copy a file path and show the path bar

## Windows
- Select the file, right-click and choose **Copy as path**, or press `Ctrl+Shift+C` in Windows 11 (gated: unconfirmed, source is paywalled or blocked). Microsoft's own pages do not document this command or shortcut; confirm on your PC.
- The result keeps quotation marks; remove them before pasting into the File Explorer address bar.
- `Alt+D`, `Ctrl+L` or `F4` select the address bar so you can read or type a path; press Enter to jump there.

## macOS
- Finder > View > **Show Path Bar** (or hold Option to show it briefly). The folders containing the item appear at the bottom of the window.
- Control-click a folder in the path bar and choose Copy "folder" as Pathname.
- `Shift+Command+G` opens Go to Folder, where you can type or paste a path.

## Gotchas
- Local paths mean nothing to other people: share a link or the file instead.

## Verify
- [ ] The pasted path opens the same folder.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Keyboard shortcuts in Windows" (Alt+D, Ctrl+L, F4); Apple Mac User Guide "Get file, folder and disk information on Mac" and keyboard shortcuts (macOS 27 / Tahoe 26, 2026). Windows Copy as path is gated because no Microsoft page confirms it. Removed unconfirmed claims: Option+Command+C, Shift-right-click on Windows 10, shell: folders, SMB path examples, dragging into Terminal.
Method: documentation only; no commands were run.
