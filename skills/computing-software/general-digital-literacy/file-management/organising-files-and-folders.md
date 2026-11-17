---
id: computing-software.general-digital-literacy.file-management.organising-files-and-folders
name: organising-files-and-folders
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, files, folders, file-explorer, windows-explorer, finder, naming-conventions, iso-8601, file-extensions, copy, move, rename, recycle-bin, trash, zip, compress, file-formats, pdf, csv, jpg, png, heic, cloud-sync, onedrive, google-drive, dropbox, icloud-drive, files-on-demand, backup, 3-2-1-backup, search]
level: intro
status: draft
description: "Organise files so you can find them in seconds: shallow folders, date-first names, visible extensions, copy vs move, formats, and cloud sync that is not a backup."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Organising files and folders — find anything in seconds, lose nothing

**Goal:** a folder structure and naming scheme you can navigate without searching, file
handling that doesn't accidentally move or overwrite things, and copies in more than
one place. Works for Windows File Explorer and macOS Finder; cloud drives behave the same.

## 1. Folder structure
- Keep it **shallow — about 3 levels**: `Work/Clients/<client>`, `Home/Finance/2026`.
  Deep trees hide files and long paths can break older Windows tools (the classic
  260-character path limit still bites some apps and zip tools).
- Organise by **what you'll look for** (area › project/year), not by file type. One
  `Archive` folder per area for finished things keeps the active list short.
- Don't use the Desktop or Downloads as storage. Process Downloads weekly: file it or delete it.

## 2. Naming convention
- **Date first, ISO style:** `2026-10-14_quote_roof-repair_v02.pdf`. `YYYY-MM-DD`
  sorts chronologically by name; `14-10-26` and `Oct 14` do not.
- Versions with leading zeros (`v01`…`v10`) so `v10` doesn't sort before `v2`. Never
  `final`, `final2`, `final-REAL` — the date and version say which is newest.
- Use letters, digits, hyphens and underscores. Avoid `\ / : * ? " < > |` (forbidden on
  Windows), and leading/trailing spaces and dots. Spaces are allowed but break some
  links and scripts.
- Rename with `F2` (Windows) or by pressing `Return` on the selected file (Mac).

## 3. Show file extensions
Extensions tell you what a file really is (`report.pdf.exe` is a program).
- Windows 11: File Explorer › View › Show › **File name extensions**
  (Windows 10: View tab › tick File name extensions).
- macOS: Finder › Settings › Advanced › **Show all filename extensions**.
Changing the extension does not convert a file; use *Save As* / *Export* in an app.

## 4. Copy vs move (the drag gotcha)
- Dragging **within the same drive moves**; dragging **to another drive or USB stick
  copies** (on both Windows and macOS). Force it: Windows `Ctrl`-drag = copy,
  `Shift`-drag = move; Mac `Option`-drag = copy, `Cmd`-drag to another volume = move.
- Safer: `Ctrl+C` / `Ctrl+X` / `Ctrl+V` (Mac `Cmd+C`, then `Cmd+Option+V` to move).
- New folder: `Ctrl+Shift+N` (Windows Explorer), `Cmd+Shift+N` (Finder).
- Deleted files go to Recycle Bin / Trash; `Shift+Delete` (Windows) bypasses it.
  Files deleted from network drives and USB sticks often skip the bin entirely.
- Zip a folder before emailing or uploading many files: right-click › Compress to ZIP
  file (Windows 11 wording; "Send to › Compressed folder" in Windows 10) or Finder ›
  Compress.

## 5. Choosing a format
| Need | Use |
|---|---|
| Final document others shouldn't edit | PDF |
| Document to keep editing | `.docx` / `.odt` / Google Doc |
| Data table for any program | CSV (plain, but loses formatting and formulas) |
| Photos | JPG (small); iPhone HEIC may need converting to JPG for older software |
| Screenshots, logos, text images | PNG (sharp edges, transparency) |

## 6. Cloud sync is not backup
- OneDrive, Google Drive, Dropbox and iCloud Drive **mirror** a folder: delete or corrupt
  a file on one device and the change syncs everywhere. They do keep deleted files and
  older versions for a limited period (often around 30 days, varying by service and plan —
  check yours) — that is your undo, not your archive.
- "Online-only" / Files On-Demand files (a cloud icon) are not on the device; mark key
  folders **Always keep on this device** before travelling offline.
- Watch for **conflict copies** (`report (1).docx`, `report-PC-conflict.docx`) when two
  devices edit at once; merge and delete them.
- **3-2-1 rule:** 3 copies, on 2 kinds of storage, 1 off-site. E.g. laptop + cloud sync +
  an external drive with File History (Windows) or Time Machine (macOS).

## 7. Finding things
- Windows Explorer search box: `*.pdf`, `datemodified:this week`, `size:>100MB`.
- macOS Spotlight (`Cmd+Space`) or Finder search: `kind:pdf`, `date:today`. Exact
  operator support varies by OS version; the filter buttons in the search bar are the
  reliable fallback.

## Verify
- [ ] Top-level folders fit on one screen; nothing is deeper than ~4 levels.
- [ ] Recent files follow `YYYY-MM-DD_description_vNN.ext` and sort correctly by name.
- [ ] File extensions are visible.
- [ ] You can state where a file goes when dragged to a USB stick vs another folder.
- [ ] Important files exist in at least two independent places, one off-site, and you
      have restored one test file from the backup.
