---
id: computing-software.general-digital-literacy.file-management.drag-and-drop-copy-or-move
name: drag-and-drop-copy-or-move
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-operations, drag-and-drop, copy-vs-move, cut-copy-paste, modifier-keys]
level: intro
status: docs-checked
description: "Force copy, move or shortcut with modifier keys when dragging in File Explorer, make Mac aliases, and use cut, copy and paste instead."
sources:
  - https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
  - https://support.apple.com/en-us/102650
  - https://support.apple.com/guide/mac-help/create-and-remove-aliases-on-mac-mchlp1046/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drag-and-drop copy vs move

**Goal:** files end up copied or moved deliberately.

## Force the action (hold while dropping a file)
- **Windows File Explorer:** hold `Ctrl` to copy, `Shift` to move, `Alt` to create a shortcut to the original.
- **Mac:** hold `Option+Command` while dragging to create an alias.
- Watch the label by the pointer to see what will happen before you release.

## Keyboard alternative
- Windows: cut, copy and paste with `Ctrl+X`, `Ctrl+C`, `Ctrl+V`.
- Mac: `Command+C`, then `Option+Command+V` moves the copied files from their original location to the current one; `Command+V` pastes a copy.

## Undo
`Ctrl+Z` (Windows) or `Command+Z` (Mac) undoes the last action; `Ctrl+Y` / `Shift+Command+Z` redo.

## Verify
- [ ] After a move the file exists only at the destination; after a copy it exists in both places.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Keyboard shortcuts in Windows" (File Explorer drag modifiers, Ctrl+Z/Y); Apple Mac User Guide keyboard shortcuts (Option-Command-V, Command-Z) and "Create and remove aliases" (macOS 27 / Tahoe 26, 2026). Removed the default-behaviour table (same drive versus other drive), Mac Option and Command drag modifiers and the Esc cancel, which no documentation fetched covers.
Method: documentation only; no commands were run.
