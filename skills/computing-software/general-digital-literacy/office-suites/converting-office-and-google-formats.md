---
id: computing-software.general-digital-literacy.office-suites.converting-office-and-google-formats
name: converting-office-and-google-formats
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, cloud-documents, convert-office-files, office-compatibility-mode, docx-to-google-docs, download-as-docx, open-in-word, convert-uploads]
level: intro
status: docs-checked
description: "Edit Word/Excel/PowerPoint files in Google Docs/Sheets/Slides (Office editing or conversion), convert back, and know which features survive the round trip."
sources:
  - https://support.google.com/docs/answer/9406611
  - https://support.google.com/drive/answer/9406611
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Converting between Office and Google formats

**Goal:** collaborate across Microsoft 365 and Google Workspace without breaking documents.

## Two ways to open an Office file in Google
1. **Office editing:** open the .docx/.xlsx/.pptx from Drive in Docs/Sheets/Slides; a file-extension chip appears next to the name. Changes auto-save to the original file in its Office format. If you use Office editing, disable the Chrome Office-editing extension to avoid compatibility problems.
2. **Convert:** make a copy as a Google file (for Excel: **File > Save as Google Sheets**; the original is unchanged). Conversion is needed for add-ons, Apps Script, protected ranges and translate options.
- To convert future uploads automatically: open Drive settings (drive.google.com/drive/settings on a computer) and tick **Convert uploads to Google Docs editor format**. Existing files are not converted, and the setting converts .doc, .docx, .html, .txt and .rtf uploads, which can break plain-text templates.

## Back to Office
In Docs/Sheets/Slides use **File > Download** and choose a file type. In Microsoft 365, save the downloaded file to OneDrive to co-author there.

## Gotchas
- Converting creates a second file: tell collaborators which one is current to avoid diverging versions.
- Open the converted or downloaded file and page through it; features differ between suites.

## Verify
- [ ] After conversion, page count, tables and charts match the original on a quick scroll-through.

## Checked

2026-10-27. Google Docs/Drive help 'Work with Microsoft Office files' (read 2026-10-27): Office editing, auto-save in original format, conversion reasons, Save as Google Sheets, Convert uploads setting and its file types, File > Download. Removed: blue .DOCX badge wording (page says file-extension chip), the lists of features that do not survive conversion, comment round-trip claims and Microsoft-side menu details (not covered by the Google page).

Method: documentation only; no commands were run.
