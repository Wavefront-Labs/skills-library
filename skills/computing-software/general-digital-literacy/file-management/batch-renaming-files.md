---
id: computing-software.general-digital-literacy.file-management.batch-renaming-files
name: batch-renaming-files
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, rename, batch-rename, bulk-rename, powerrename, finder-rename, numbering-files, photo-renaming]
level: intro
status: docs-checked
description: "Rename many files at once with File Explorer, PowerToys PowerRename or macOS Finder's Rename Items (replace text, add dates, sequential numbers)."
sources:
  - https://support.apple.com/guide/mac-help/rename-files-folders-and-disks-on-mac-mchlp1144/mac
  - https://learn.microsoft.com/en-us/windows/powertoys/powerrename
  - https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Batch renaming files

**Goal:** turn `IMG_4412.JPG ... IMG_4498.JPG` into `2026-08 Holiday 01.jpg ...` in one go.

## Windows File Explorer
- `F2` renames the selected item.

## Windows PowerToys PowerRename
- Select files in File Explorer, right-click > **Rename with PowerRename** (it appears only if enabled in PowerToys). A preview pane shows the search and replace results before you apply them.
- Options: plain text replace or **Use regular expressions** (ECMAScript grammar), enumerate items with `${start=X}` counters, and date tokens such as `$YYYY`, `$MM`, `$DD` (taken from the file's date).

## macOS Finder
- Select the files, Control-click one and choose **Rename**. In the Rename Finder Items pop-up choose:
  - *Replace Text* in the names,
  - *Add Text* before or after the current name,
  - *Format*: pick a name format, put the index, counter or date before or after the name, enter a custom format name and the number to start from.
- Click **Rename**.

## Gotchas
- Do not rename files that other programs find by path (library internals, linked project files).
- Keep names sortable: dates as `YYYY-MM-DD`, padded numbers (`01`, `02`).

## Verify
- [ ] Sorted by name, the files are in the order you want with no duplicates or lost extensions.

## Checked
Date: 2026-10-27. Documentation: Apple Mac User Guide "Rename files, folders and disks on Mac" (macOS 27 / Tahoe 26, 2026); Microsoft Learn PowerToys PowerRename page; Microsoft Support "Keyboard shortcuts in Windows" (F2). Removed unconfirmed claims: Explorer multi-file F2 naming pattern, winget package id, undo of a whole batch.
Method: documentation only; no commands were run.
