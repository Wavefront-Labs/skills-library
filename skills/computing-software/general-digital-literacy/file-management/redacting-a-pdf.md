---
id: computing-software.general-digital-literacy.file-management.redacting-a-pdf
name: redacting-a-pdf
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-scanning, redact-pdf, redaction, black-out-text]
level: intro
status: draft
description: "Permanently remove names, account numbers and other text from a PDF with true redaction tools, and avoid the black-box mistake that leaves the text copyable."
sources:
  - https://helpx.adobe.com/acrobat/using/removing-sensitive-content-pdfs.html
  - https://www.nsa.gov/portals/75/documents/what-we-do/cybersecurity/professional-resources/csi-redacting-pdf-files.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Redact a PDF

Drawing a black rectangle (or highlighting in black) **hides** text but leaves it underneath: anyone can copy-paste or remove the box. Real redaction deletes the content.

## Tools that truly redact
- **Adobe Acrobat Pro:** Tools › **Redact** › *Redact text & images* › mark items (or *Find text* for every occurrence of an account number) › **Apply** › save as a new file. Also run *Sanitize Document* to remove metadata, hidden layers and comments.
- **Mac Preview (macOS 11+):** Tools › **Redact** › drag over text; saved file removes the text.
- **PDF24 Creator / Stirling-PDF** (free, local): redact tools that remove text.
- Low-tech but safe: print, black out with a marker, **scan** the result (scans contain no text layer unless OCR'd).

## Process
1. Work on a copy; keep the original private.
2. Search the document for every instance (names, numbers, emails, addresses in headers/footers).
3. Apply redactions, then save as new file.
4. Remove metadata: Acrobat Sanitize; Word source file › Inspect Document before exporting.

## Gotchas
- Redacting in Word with black highlight then exporting to PDF keeps the text.
- Scanned PDFs with OCR have an invisible text layer; redact it too (Acrobat handles both).
- File names and bookmarks can leak too.

## Verify
- [ ] In the saved copy, select-all + paste into Notepad and search (`Ctrl+F`) for the redacted words: nothing is found.
