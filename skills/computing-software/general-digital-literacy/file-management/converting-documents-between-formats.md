---
id: computing-software.general-digital-literacy.file-management.converting-documents-between-formats
name: converting-documents-between-formats
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-formats, document-conversion, file-conversion, pdf-to-word, image-formats, heic-to-jpg]
level: intro
status: draft
description: "Convert files between common formats (Word, PDF, ODT, RTF, images, HEIC to JPG, audio and video) with built-in tools, and check what gets lost in the conversion."
sources:
  - https://support.microsoft.com/en-us/word
  - https://help.libreoffice.org/latest/en-US/text/shared/main0000.html
  - https://support.apple.com/guide/mac-help/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Convert documents between formats

**Goal:** the recipient can open and use the file, with nothing important lost.

## Documents
| From → to | Built-in way |
|---|---|
| Word → PDF | File › Save As / Export › PDF (Word, Google Docs Download › PDF, LibreOffice Export as PDF) |
| PDF → Word | Word: File › Open the PDF (converts, layout may shift); Google Drive: right-click › Open with Docs; Acrobat Export PDF |
| ODT/RTF ↔ DOCX | Open in Word or LibreOffice › Save As the other format |
| Pages/Numbers/Keynote → Office | File › Export To › Word/Excel/PowerPoint |
| Many files at once | `soffice --headless --convert-to pdf *.docx` (LibreOffice command line) |

## Images
- **HEIC (iPhone) → JPG:** iPhone Settings › Camera › Formats › *Most Compatible*, or Settings › Photos › Transfer to Mac or PC › *Automatic*; Mac Preview › File › Export › JPEG; Windows Photos › Save as.
- PNG ↔ JPG: Paint or Photos (Windows) › Save as; Preview (Mac) › Export.
- Several images: Mac Finder select › right-click › **Quick Actions › Convert Image**.

## Audio and video
Mac: right-click › *Encode Selected Video Files*. Windows: Clipchamp export. VLC: Media › Convert/Save handles most formats.

## What gets lost
- PDF → Word: fonts, columns and tables often shift; scanned PDFs need OCR first.
- Word → ODT/Google Docs: tracked changes, macros, some fields and SmartArt may change.
- JPG is lossy; keep the original. PNG for screenshots and text.

## Safety
Online converters upload your file to someone else's server; avoid them for anything personal or confidential.

## Verify
- [ ] Open the converted file in the recipient's likely app and check page count, tables, images and fonts.
