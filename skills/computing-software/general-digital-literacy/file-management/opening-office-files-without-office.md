---
id: computing-software.general-digital-literacy.file-management.opening-office-files-without-office
name: opening-office-files-without-office
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-formats, open-docx-without-word, libreoffice, free-office-viewers]
level: intro
status: draft
description: "Open, read and edit .docx, .xlsx and .pptx files without paying for Microsoft Office using Office for the web, Google Docs, Apple iWork or LibreOffice, and what formatting breaks."
sources:
  - https://www.microsoft365.com/
  - https://www.libreoffice.org/discover/libreoffice/
  - https://support.google.com/docs
  - https://support.apple.com/pages
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Open Office files without Office

## Free options
- **Microsoft 365 for the web** (microsoft365.com, free Microsoft account): Word, Excel and PowerPoint in a browser, full fidelity for most documents. Upload to OneDrive or open from an email attachment.
- **Google Docs/Sheets/Slides**: upload to Drive, double-click; edit in Office mode (keeps .docx) or *File > Save as Google Docs*.
- **Apple Pages, Numbers, Keynote** (free on Mac/iPhone/iPad): open Office files and export back to Office format (*File > Export To > Word*).
- **LibreOffice** (Windows/Mac/Linux, free, offline): Writer, Calc, Impress open and save .docx/.xlsx/.pptx.
- **Mobile**: Microsoft 365 app (free for viewing; editing free on phones under 10.1 inches), Google Docs/Sheets apps, Files/Quick Look previews.
- Just viewing: email apps and Windows/Mac preview (Quick Look, space bar) show most documents.

## What breaks
- Complex layout: text boxes, SmartArt, tracked changes edge cases, specific fonts (substituted), macros (.xlsm VBA won't run outside Excel desktop), pivot tables/Power Query in non-Microsoft apps.
- Round-tripping (open, save, send back) through another suite can shift pagination; send a PDF too if layout matters.

## Tips
- Install common free fonts (Calibri/Aptos substitutes: Carlito) in LibreOffice for closer layout.
- Old .doc/.xls formats open fine in all of these.

## Verify
- [ ] The file opens, edits save in the original format, and the recipient confirms it looks right.
