---
id: computing-software.general-digital-literacy.file-management.file-in-use-cannot-delete
name: file-in-use-cannot-delete
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-operations, file-in-use, locked-file, access-denied]
level: intro
status: docs-checked
description: "Delete, rename or move a file Windows says is open in another program, or a Mac says is in use, by finding the app holding it, and when a restart is simplest."
sources:
  - https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
  - https://learn.microsoft.com/en-us/windows/powertoys/file-locksmith
  - https://support.apple.com/en-us/102650
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# File in use and cannot be deleted

## Windows
1. Close the app that has the file open (check the taskbar and system tray).
2. Close the Preview pane (`Alt+P`) in case it is holding the file.
3. Microsoft PowerToys **File Locksmith** shows which processes use a file: turn on *Enable File Locksmith* in PowerToys, select the file or folder in File Explorer, right-click > **Show more options** > **Unlock with File Locksmith**.
4. Still stuck: restart and delete before opening anything.
- "Access is denied" is a permissions problem, not a file lock; do not take ownership of system folders.

## Mac
- Quit the app using the file; Force Quit is `Option+Command+Esc`. Then empty the Trash; restart if it persists.

## Verify
- [ ] The file deletes or renames without an error.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "Keyboard shortcuts in Windows" (Alt+P), Microsoft Learn PowerToys File Locksmith page, and Apple Mac User Guide keyboard shortcuts (Option-Command-Esc; macOS 27 / Tahoe 26, 2026). Removed unconfirmed claims: Resource Monitor and Process Explorer steps, owner files, error message wording, ownership steps and the lsof command.
Method: documentation only; no commands were run.
