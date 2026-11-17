---
id: computing-software.general-digital-literacy.file-management.finding-large-files-to-free-space
name: finding-large-files-to-free-space
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-search, find-large-files, disk-space, storage]
level: intro
status: docs-checked
description: "Find what is filling a disk with Windows Storage settings and Mac storage tools, then delete or move it safely."
sources:
  - https://support.microsoft.com/en-us/windows/free-up-drive-space-in-windows-85529ccb-c365-490d-b548-831022bc9b32
  - https://support.apple.com/en-us/102624
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Find large files to free space

## Windows
1. Open Settings, System, **Storage**: it shows what uses space and offers **Cleanup recommendations** (Microsoft Support).
2. **Temporary files** (and Disk Cleanup) clear items you do not need; **Storage Sense** can free space automatically,
   including temporary files and the Recycle Bin.
3. Sort a folder in File Explorer by Size to find the largest items; disk-usage mapping tools (for example WizTree or
   WinDirStat) show every folder by size. Typical culprits are Downloads, old phone backups, video projects and game libraries.

## Mac
Apple's guide covers checking available space, **Optimize Storage**, and moving or deleting files. Open the Storage settings
on your Mac (menu paths vary by macOS version) and review each category by size.

## Safe deletion rules
- Delete your own files (downloads, duplicate videos, old installers). Do **not** delete system files or folders such as
  WinSxS, pagefile.sys or hiberfil.sys.
- Before deleting anything you cannot replace, copy it to an external drive or cloud and check that it opens there
  (back-up first); then delete the original.
- Empty the Recycle Bin/Trash afterwards.

## Verify
- [ ] Free space shown in Storage settings rose by the expected amount.

## Checked
2026-10-28. Confirmed (Microsoft Support, Free up drive space in Windows; Apple Support 102624): Storage settings and Cleanup
recommendations, temporary files, Disk Cleanup, Storage Sense, Mac Optimize Storage and "move or delete files" guidance.
Removed (unconfirmed): `size:gigantic`/`size:>1GB` search syntax, backup folder path, Finder Cmd+F recipe, "free" claim
for third-party tools, 15-20 percent free-space target, per-version Mac menu paths.
Method: documentation only; no commands were run.
