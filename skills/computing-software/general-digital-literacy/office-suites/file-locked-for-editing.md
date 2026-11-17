---
id: computing-software.general-digital-literacy.office-suites.file-locked-for-editing
name: file-locked-for-editing
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, cloud-documents, collaborative-editing, file-locked-for-editing, co-authoring, upload-blocked]
level: practitioner
status: docs-checked
description: "Fix 'file is locked for editing by another user' and co-authoring failures in Word and Excel: stale locks, unsupported versions, locations, formats and features."
sources:
  - https://support.microsoft.com/en-us/excel/excel-file-is-locked-for-editing
  - https://support.microsoft.com/en-us/excel/get-started/collaborate-on-excel-workbooks-at-the-same-time-with-co-authoring
  - https://support.microsoft.com/en-us/word/the-document-is-locked-for-editing-by-another-user-error-message-when-you-try-to-open-a-document-in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# File locked for editing

## Message: "locked for editing by another user"
Work through these in order (Excel guidance; most applies to Word and PowerPoint too):
1. **Locked by you:** close the file on all your devices, then wait a few minutes for the server to
   release the lock.
2. **Someone else really has it open:** wait until they close it, open it read-only, or ask them to close
   it, check it in, or give you edit permission. Microsoft 365 also offers *Request more access*, which
   emails the owner.
3. **A version that can't co-author:** everyone needs Microsoft 365 (signed in) or the web app. Excel
   2016, 2019 and 2021 LTSC don't co-author, and if even one person uses one, everyone else gets the
   "locked" error.
4. **Wrong location:** co-authoring needs OneDrive, OneDrive for Business or SharePoint in Microsoft 365.
   Local folders and SharePoint on-premises libraries lock instead. If you sync with the OneDrive app,
   keep it up to date and not paused.
5. **Wrong format (Excel):** co-authoring needs `.xlsx`, `.xlsm` or `.xlsb` (not Strict Open XML); use
   File › Save a Copy to convert.
6. **Unsupported features (Excel):** turn off the legacy **Shared Workbook** feature, remove password
   encryption or restricted access (File › Info › Protect Workbook), and untick *Refresh data when opening
   file* on tables and PivotTables.

## Stale owner file (Word, files on a network or local folder)
Word creates a temporary owner file next to the document, named `~$` plus the rest of the file name. If
Word quit improperly it can be left behind and cause the lock. First confirm nobody else has the document
open; then quit all instances of Word (end any leftover Word process in Task Manager) and delete the
owner file from the document's folder.

## Verify
- [ ] Two people open the file: each sees the other's presence and AutoSave is on.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365 and Word) as published on that date:
  locked-by-you and other-user steps, Request more access, co-authoring versions and the LTSC note,
  supported and unsupported locations, OneDrive sync app advice, file formats, Shared Workbook /
  encryption / refresh-on-open features, the Word owner file name, cause and removal steps.

Method: documentation only; no commands were run.
