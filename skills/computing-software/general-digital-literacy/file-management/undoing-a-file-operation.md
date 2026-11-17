---
id: computing-software.general-digital-literacy.file-management.undoing-a-file-operation
name: undoing-a-file-operation
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-operations, undo-file-operation, undo-delete, undo-move]
level: intro
status: docs-checked
description: "Undo an accidental move, rename, copy or delete in File Explorer and Finder with Ctrl+Z or Command+Z, and know what to try when undo is no longer available."
sources:
  - https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
  - https://support.apple.com/en-us/102650
  - https://support.apple.com/en-us/109344
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Undo a file operation

## Immediately
- **Windows:** `Ctrl+Z` undoes the previous action in File Explorer; `Ctrl+Y` redoes it.
- **Mac:** Finder > Edit > **Undo** (`Command+Z`); `Shift+Command+Z` redoes.

## When undo is not available
- A permanent delete (`Shift+Delete` in File Explorer) skips the Recycle Bin; plain `Delete` or `Ctrl+D` moves the item to the Recycle Bin, where it can be restored.
- Files in iCloud Drive Desktop and Documents folders: deleting on one device deletes everywhere, but deleted files stay in Recently Deleted (Files app or iCloud.com) for 30 days.
- Moved somewhere unknown: search by name or sort by date modified; on a Mac use `Shift+Command+F` for Recents.

## Gotchas
- Undo acts on the last action, which may not be the one you expect; check before repeating it.

## Verify
- [ ] The file is back in its original folder with its original name.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Keyboard shortcuts in Windows" (Ctrl+Z, Ctrl+Y, Delete, Shift+Delete); Apple Mac User Guide keyboard shortcuts (Command-Z, Shift-Command-Z, Shift-Command-F) and Apple Support "Add your Desktop and Documents files to iCloud Drive" (30 days Recently Deleted) (macOS 27 / Tahoe 26, 2026). Removed unconfirmed claims: right-click Undo label, Trash Put Back, Previous Versions and third-party recycle bins.
Method: documentation only; no commands were run.
