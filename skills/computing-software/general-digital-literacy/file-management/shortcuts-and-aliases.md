---
id: computing-software.general-digital-literacy.file-management.shortcuts-and-aliases
name: shortcuts-and-aliases
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-operations, desktop-shortcuts, aliases, symbolic-links]
level: intro
status: docs-checked
description: "Create shortcuts on Windows (Alt-drag) and aliases on Mac (Make Alias), and know a shortcut is a pointer, not a copy of the file."
sources:
  - https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
  - https://support.microsoft.com/en-us/windows/experience/fileexplorer/file-explorer-in-windows
  - https://support.apple.com/guide/mac-help/create-and-remove-aliases-on-mac-mchlp1046/mac
  - https://support.apple.com/en-us/102650
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Shortcuts and aliases

## Windows
- Hold `Alt` while dragging a file in File Explorer to create a shortcut to the original in the drop location.
- Windows 11 shows a streamlined context menu; the full older menu is under **Show more options** (also `Shift+F10`, or Shift plus right-click).

## Mac
- Select the item and choose File > **Make Alias** (`Control+Command+A`). Press `Option+Command` while dragging the original to create an alias and move it in one step.
- With an alias selected in the Finder, `Command+R` shows the original.
- Items in the Finder sidebar and Dock are aliases to the originals; removing one removes only the alias.
- Opening an alias opens the original item.

## Gotchas
- A shortcut or alias is a pointer, not a copy: backing up or emailing it does not include the file itself.

## Verify
- [ ] Double-clicking opens the original; deleting the shortcut leaves the original intact.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Keyboard shortcuts in Windows" and "File Explorer in Windows"; Apple Mac User Guide "Create and remove aliases on Mac" and keyboard shortcuts (macOS 27 / Tahoe 26, 2026). Removed unconfirmed claims: Create shortcut menu item wording, .lnk details, Shortcut key box, website drag, broken-link error text and Fix Alias, symlink commands.
Method: documentation only; no commands were run.
