---
id: computing-software.general-digital-literacy.file-management.editing-text-in-a-pdf
name: editing-text-in-a-pdf
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-scanning, edit-pdf, pdf-editor, acrobat]
level: intro
status: draft
description: "Change text in a PDF with Acrobat, Word's PDF reflow, Preview, LibreOffice Draw or online editors, and know when to edit the source document instead."
sources:
  - https://helpx.adobe.com/acrobat/using/edit-text-pdfs.html
  - https://support.microsoft.com/en-us/word
  - https://support.apple.com/guide/preview/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Edit text in a PDF

## Best option: edit the source
- If you have the original Word/Docs file, edit that and export a new PDF. PDF editing is a patch, not a rewrite.

## Tools
- **Adobe Acrobat (paid)**: **Edit PDF** tool; click into text, type; fonts matched if installed. Scanned PDFs are OCR'd first. Acrobat online offers limited free edits.
- **Microsoft Word**: *File > Open* the PDF; Word converts it to editable text (layout may shift with complex pages). Save as Word or back to PDF.
- **Mac Preview**: can't edit existing text; add text boxes (Markup > *Text*) and white rectangles to cover. Fine for forms and small corrections.
- **LibreOffice Draw**: opens PDFs as editable objects line by line; good for small changes, slow for many.
- **Online editors** (Smallpdf, iLovePDF, PDF24): convenient; avoid for confidential documents.

## Covering vs removing
- A white box over text hides it visually but the text is still in the file. To truly remove sensitive text, use **redaction** (Acrobat *Redact*, or see the redaction skill).

## Gotchas
- Missing fonts get substituted, so edited lines may look different.
- Signed or certified PDFs: editing invalidates the signature.
- Forms: fill fields instead of editing text.
- Altering official documents you didn't issue (certificates, statements) may be fraud.

## Verify
- [ ] Reopen in a different viewer: edits show, layout intact, and removed text can't be found with Ctrl+F.
