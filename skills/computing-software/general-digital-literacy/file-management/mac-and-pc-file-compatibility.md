---
id: computing-software.general-digital-literacy.file-management.mac-and-pc-file-compatibility
name: mac-and-pc-file-compatibility
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-formats, cross-platform-files, mac-pc-compatibility, exfat, iwork]
level: intro
status: docs-checked
description: "Share files between Mac and Windows without surprises: Pages/Numbers/Keynote exports, HEIC photos, exFAT drives, zip junk files and fonts that do not travel."
sources:
  - https://support.apple.com/guide/pages/export-to-word-pdf-or-another-file-format-tan8d1b2a8f/mac
  - https://support.apple.com/guide/disk-utility/format-a-disk-for-windows-computers-dskutl1010/mac
  - https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mac and PC file compatibility

## Documents
- Pages, Numbers and Keynote files can be exported to Word, PDF or another format from the app (see Apple's Pages guide "Export to Word, PDF or another file format"). Send a PDF when layout must not change.

## Drives
- Apple's Disk Utility guidance for Windows-compatible disks: **MS-DOS (FAT)** for volumes of 32 GB or less, **ExFAT** for volumes over 32 GB. APFS is the default format for Macs on macOS 10.13 or later.
- Format a shared drive in Disk Utility with a Windows-compatible format.

## Names
- Windows rejects `< > : " / \ | ? *` in names and names ending with a space or period; rename files before copying them from a Mac.

## Verify
- [ ] The recipient opens the file on the other platform with layout, images and names intact.

## Checked
Date: 2026-10-27. Documentation: Apple Disk Utility User Guide "Format a disk for Windows computers" and "File system formats", Apple Pages User Guide export page title, Microsoft Learn "Naming Files, Paths, and Namespaces" (macOS 27 / Tahoe 26 era, 2026). Removed unconfirmed claims: iCloud.com access for Windows users, HEIC and Transfer to Mac or PC settings, mov codecs, NTFS read-only on Mac, DS_Store and __MACOSX files, Cmd versus Ctrl mapping.
Method: documentation only; no commands were run.
