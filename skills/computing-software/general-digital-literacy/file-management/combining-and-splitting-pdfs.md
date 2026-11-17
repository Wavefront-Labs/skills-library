---
id: computing-software.general-digital-literacy.file-management.combining-and-splitting-pdfs
name: combining-and-splitting-pdfs
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, scanning, pdf, merge-pdfs, split-pdf, reorder-pages, extract-pages, preview-app, pdf24, acrobat]
level: intro
status: draft
description: "Merge several PDFs into one, split out or reorder pages and delete pages using macOS Preview, Microsoft Edge/print-to-PDF, Acrobat or offline tools like PDF24."
sources:
  - https://support.apple.com/guide/mac-help/welcome/mac
  - https://helpx.adobe.com/acrobat/using/merging-files-single-pdf.html
  - https://tools.pdf24.org/en/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Combining, splitting and reordering PDFs

**Goal:** turn scattered PDFs into one tidy file, or pull out just the pages you need.

## Mac: Preview (built in)
- Open the first PDF › View › **Thumbnails** › drag other PDF files into the sidebar where they
  should go › File › Export as PDF (or Save).
- Reorder: drag thumbnails. Delete: select thumbnail › `Delete`. Rotate: `Cmd+R`/`Cmd+L`.
- Extract pages: select thumbnails › drag them to the Desktop (creates a new PDF).

## Windows
- **Extract or reorder pages** of one PDF: open in Edge/Chrome › Print › choose pages (`2-4`) ›
  Microsoft Print to PDF / Save as PDF.
- **Merge** needs a tool: Adobe Acrobat (paid: Tools › Combine Files), **PDF24 Creator** (free,
  works offline), or PDFsam Basic (free, open source).
- Word can open PDFs for editing but reflows layout; not for merging.

## Online tools
Many websites merge PDFs free. Avoid uploading ID documents, contracts, medical or financial PDFs to
unknown services; use an offline tool for those.

## Gotchas
- Forms and signatures may break when merged; flatten or merge the final signed copies only.
- Merged scans can be large: compress (Preview › Export › Quartz Filter: Reduce File Size; PDF24 Compress).

## Verify
- [ ] Page count of the result = sum of inputs (minus deleted); pages in the right order and upright.
