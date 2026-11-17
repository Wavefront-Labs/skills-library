---
id: computing-software.general-digital-literacy.file-management.replace-or-skip-duplicate-names
name: replace-or-skip-duplicate-names
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-operations, file-name-conflict, replace-or-skip, keep-both, merge-folders]
level: intro
status: draft
description: "Handle the replace, skip or keep both prompt when copying files with the same name in File Explorer and Finder, merge folders safely, and avoid overwriting newer work."
sources:
  - https://support.microsoft.com/en-us/windows
  - https://support.apple.com/guide/mac-help/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Replace or skip duplicate names

**Goal:** copying into a folder never silently overwrites a newer version.

## Windows
"The destination already has a file named…":
- **Replace the files in the destination** overwrites.
- **Skip these files** keeps the destination copy.
- **Let me decide for each file**: shows both with **size and date modified**; tick left, right, or both (both keeps the copy as `name (2).ext`). Tick *Skip files with the same date and size*.
- Folders with the same name **merge** automatically; Windows asks only about individual clashing files.

## Mac Finder
- File clash: **Keep Both** (adds " 2"), **Stop**, **Replace**. Tick *Apply to all*.
- Folder clash: **Replace** deletes the whole destination folder and its contents. Hold **Option** while dragging to get **Merge**, which keeps newer files and adds missing ones. Only offered when the source has files the destination lacks.

## Cloud drives
OneDrive/Google Drive uploads: *Replace* keeps version history (old version restorable), *Keep both* uploads a copy with a number.

## Safer habits
- Compare the date modified before choosing; newer usually wins, but check.
- For big folder syncs (backups to USB), use a tool that only copies newer files: `robocopy src dst /E /XO` (Windows, skips older) or `rsync -av --update src/ dst/` (Mac/Linux).
- Version important files in names (`report-v3.docx`) or rely on cloud version history.

## Verify
- [ ] After copying, open the kept file and confirm it's the newer version.
