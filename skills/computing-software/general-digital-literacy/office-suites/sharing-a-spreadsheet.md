---
id: computing-software.general-digital-literacy.office-suites.sharing-a-spreadsheet
name: sharing-a-spreadsheet
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, share-spreadsheet, view-only, comment-only, co-authoring, onedrive-share, google-sheets-share, edit-history]
level: intro
status: docs-checked
description: "Share an Excel or Google Sheets spreadsheet with view, comment or edit access, co-edit live, see who changed a cell and avoid emailing conflicting copies."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/collaborate-on-excel-workbooks-at-the-same-time-with-co-authoring
  - https://support.microsoft.com/en-us/excel/excel-file-is-locked-for-editing
  - https://support.microsoft.com/en-us/excel/show-changes-that-were-made-in-a-workbook
  - https://support.google.com/drive/answer/7166529?hl=en
  - https://support.google.com/docs/answer/190843?hl=en
  - https://support.google.com/docs/answer/3540681?hl=en
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing a spreadsheet and controlling editing

**Goal:** one live copy everyone works on, with the right level of access.

## Share
- **Excel:** the workbook must be on **OneDrive, OneDrive for Business or SharePoint Online**
  (SharePoint on-premises sites and local folders don't support co-authoring) and saved as `.xlsx`,
  `.xlsm` or `.xlsb`. Select **Share** (upper-right) › type email addresses, or **Share › Copy link** to
  send the link yourself.
- **Google Sheets:** **Share** › add people as *Viewer*, *Commenter* or *Editor*; general access is
  *Restricted* (only people added) or *Anyone with the link*.

## Co-editing
- Excel: keep **AutoSave** on (upper-left). Everyone needs a version that supports co-authoring
  (Microsoft 365 or Excel for the web; Excel 2016, 2019 and 2021 LTSC don't). In Microsoft 365, the web
  and mobile apps you see other people's selections in different colours.
- Google Sheets: a normal filter changes the view for everyone; use **Data › Create filter view** for
  your own view.

## Who changed this?
- Google Sheets: right-click a cell › **Show edit history**; some changes (for example formatting) may
  not appear. File-level history is in version history.
- Excel for Microsoft 365: **Review › Show Changes** lists who changed what and when (past 365 days);
  right-click a sheet, range or cell › *Show Changes* to narrow it.

## Gotchas
- Emailing attachments creates divergent copies ("final_v3_JS.xlsx"). Share a link instead.
- "Anyone with the link" can open the file without signing in; use named people for personal data.
- Google editors can change permissions and re-share by default: Share › **Settings** › untick *Allow
  editors to change permissions and share*.
- In Excel, the legacy **Shared Workbook** feature blocks co-authoring; turn it off.

## Verify
- [ ] Open the link in a private window (or ask a colleague): access level is what you chose.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Drive Help and Google Docs
  Editors Help as published on that date: co-authoring locations, file formats, Share / Copy link,
  AutoSave, supported versions, coloured selections, Show Changes path, 365-day window and right-click
  scope, Shared Workbook blocking; Google roles, link access options, editor re-share setting, Show edit
  history and its gaps, filter views.

Method: documentation only; no commands were run.
