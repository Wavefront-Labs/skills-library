---
id: computing-software.general-digital-literacy.office-suites.encrypt-workbook-with-password
name: encrypt-workbook-with-password
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, print-spreadsheet, protect-sheet, encrypt-workbook, protect-workbook-structure, file-password]
level: practitioner
status: docs-checked
description: "Require a password to open an Excel workbook, protect workbook structure, and know how this differs from sheet protection and Google Sheets sharing."
sources:
  - https://support.microsoft.com/en-us/office/protect-an-excel-file-7359d4ae-7213-4ac2-b058-f75e9311b599
  - https://support.microsoft.com/en-us/office/protect-a-workbook-7e365a4d-3e89-4616-84ca-1931257c1517
  - https://support.microsoft.com/en-us/excel/protect-a-worksheet
  - https://support.microsoft.com/en-us/excel/protection-and-security-in-excel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Encrypt a workbook with a password

| Layer | Stops | Menu |
|---|---|---|
| **Encrypt with Password** | Opening the file without the password | File › Info › Protect Workbook |
| Protect Workbook (structure) | Adding, moving, deleting, hiding, renaming sheets | Review › Protect Workbook |
| Protect Sheet | Editing locked cells | Review › Protect Sheet |

## Encrypt
Windows: **File › Info › Protect Workbook › Encrypt with Password** › type › confirm › save.
- Passwords are case-sensitive. Microsoft cannot retrieve a forgotten or lost password, so store
  it in a password manager.
- Share the password by another channel (phone/SMS), not in the same message as the file.

## Gotchas
- Microsoft says worksheet protection is not a security feature: it only prevents changes to
  locked cells. Only encryption protects confidentiality.
- Passwords cannot be added, changed, removed or recovered in Excel for the web.

## Verify
- [ ] Close and reopen: password prompt appears before any content shows.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft Protect an Excel file and Protect a workbook pages (Protect Workbook, Encrypt with Password; passwords are case-sensitive; Microsoft cannot retrieve a lost password; passwords cannot be added, changed or removed in Excel for the web), Protect a worksheet (sheet protection is not a security feature), structure protection (Review, Protect Workbook).
Method: documentation only; no commands were run.
