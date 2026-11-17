---
id: computing-software.general-digital-literacy.office-suites.saving-documents-in-other-formats
name: saving-documents-in-other-formats
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, save-as-formats, document-setup, docx, odt, rtf, pdf, save-as, compatibility-mode, google-docs-download, libreoffice-writer]
level: intro
status: draft
description: "Save or download a document as DOCX, ODT, RTF, PDF or plain text in Word, Google Docs and LibreOffice, and pick the format the recipient can actually open."
sources:
  - https://support.microsoft.com/en-us/word
  - https://support.google.com/docs
  - https://help.libreoffice.org/latest/en-US/text/shared/main0000.html
  - https://icdl.org/programmes/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Saving a document in another format

**Goal:** hand someone a file they can open and that looks the way you meant it.

## Which format for which job
| Recipient needs to... | Send | Why |
|---|---|---|
| Read or print it, not change it | **PDF** | Layout and fonts frozen on every device |
| Edit it in Word / Google Docs | **DOCX** | The default everywhere since Office 2007 |
| Edit it in LibreOffice / an open-standards office | **ODT** | OpenDocument, ISO/IEC 26300 |
| Open it in anything, very old software | **RTF** or **TXT** | RTF keeps basic formatting; TXT keeps only words |
| Publish on a website | PDF, or paste into the site editor | Avoid DOCX downloads on the web |

## How
- **Word (Windows/Mac):** File › Save As (or `F12` on Windows) › Browse › "Save as type" list › choose
  *Word Document (.docx)*, *PDF*, *OpenDocument Text (.odt)*, *Rich Text Format* or *Plain Text*.
  For PDF, File › Export › Create PDF/XPS keeps headings as PDF bookmarks if you tick
  Options › "Create bookmarks using Headings".
- **Google Docs:** File › Download › Microsoft Word (.docx), OpenDocument (.odt), Rich text (.rtf),
  PDF, Plain text, Web page or EPUB. The original stays in Drive as a Google Doc.
- **LibreOffice Writer:** File › Save As › "File type" list (keep the "Use Word 2007-365!" answer
  when it asks about format); File › Export as › Export as PDF for PDF.

## Gotchas
- An old `.doc` opened in modern Word shows **[Compatibility Mode]** in the title bar. File › Info ›
  Convert upgrades it to `.docx`; do this before heavy editing so new features are available.
- Fonts the recipient doesn't have are substituted in DOCX/ODT, so line breaks move. If the look
  matters, send PDF (fonts are embedded).
- Converting between DOCX and ODT can move complex layouts (text boxes, tracked changes, fields).
  Open the result and page through it before you send.
- Saving as TXT discards images, tables and formatting with no undo once you close the file;
  keep the original.

## Verify
- [ ] File name shows the expected extension (turn on extensions in File Explorer/Finder).
- [ ] You reopened the exported copy and it looks right.
