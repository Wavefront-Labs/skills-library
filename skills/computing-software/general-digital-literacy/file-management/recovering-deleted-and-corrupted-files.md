---
id: computing-software.general-digital-literacy.file-management.recovering-deleted-and-corrupted-files
name: recovering-deleted-and-corrupted-files
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-recovery, deleted-files, recycle-bin, trash, corrupted-file, unsaved-document, autorecover, previous-versions, version-history, data-recovery-software, overwritten-file, restore-previous-version]
level: intro
status: docs-checked
description: "Get back a file you deleted, overwrote or that won't open — Recycle Bin/Trash, version history, AutoRecover, and when to stop and call a professional."
sources:
  - https://support.google.com/drive/answer/2375102
  - https://support.google.com/docs/answer/190843
  - https://support.microsoft.com/en-us/office/repair-a-corrupted-workbook-153a45f4-6cab-44b1-93ca-801ddcd4ea53
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Recovering deleted and corrupted files — before reaching for paid tools

**Goal:** recover a single lost or broken file using the free options built into your
system and apps first, and know when to stop and involve a professional. For
whole-system restore points, see basic-troubleshooting.backup-and-system-recovery; this
skill is about one file.

## 1. The first rule: stop using the drive
The moment you realise a file is gone, **stop saving anything new to that drive**. A
deleted file's data can remain until something overwrites that space, so every new save
or download risks destroying it. (General data-recovery practice; not a vendor claim.)

## 2. Recycle Bin / Trash
Check the system's Recycle Bin (Windows) or Trash (macOS) first and restore from there.
Apple's Mac help links its restore-files steps from the Files and folders section of the
Mac User Guide; follow those for your macOS version.

## 3. Overwritten document
- **Google Docs/Sheets/Slides:** click "Last edit" at the top right to browse version
  history, choose a version in the right panel and click "Restore this version", then
  confirm. "Make a copy" on a version saves an editable copy instead. You need edit
  permission to view version history. Restoring a spreadsheet version clears the
  cell-level edit history from before the restore, so make a copy if you need that
  history.
- Other suites and local files: use that product's own version-history or autosave
  help. A local file only holds what was last saved.

## 4. A file deleted beyond the Recycle Bin/Trash
- Check the cloud service's own trash. Google Drive's Trash deletes files forever after
  30 days, and trashed files still count toward storage until then. Other services
  have their own retention; check each one's help.
- If the file is gone from everywhere and it matters, stop using the drive (section 1)
  and consider a recovery tool, acting quickly; success depends on how much has
  overwritten that space.

## 5. A file that won't open ("corrupted")
- Try a different app or version of the app first.
- Excel: File › Open, select the workbook, click the arrow next to **Open**, choose
  **Open and Repair**, then **Repair**; if that fails, **Extract Data** pulls out values
  and formulas.
- If the drive shows signs of hardware failure, stop DIY attempts and consider a
  professional data-recovery service if the content justifies the cost.

## Verify
- [ ] You checked the Recycle Bin/Trash and the cloud service's own deleted-items page
      before concluding a file is unrecoverable.
- [ ] No new files were saved to the affected drive while recovery was still possible.
- [ ] For an overwritten document, version history (not just in-app undo) was checked.

## Checked
2026-11-01. Confirmed from Google Drive Help on Trash (30 days, storage), Google Docs
Editors Help on version history (Last edit, restore, copy, limits) and Microsoft's Excel
Open and Repair steps. Removed: Windows and macOS Trash click paths, Shift+Delete and
USB behaviour, Word AutoRecover menu paths, OneDrive/SharePoint history, ~30-day figures
for other services, named recovery tools, and sync-interruption claims.
Method: documentation only; no commands were run.
