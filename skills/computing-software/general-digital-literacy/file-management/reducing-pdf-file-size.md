---
id: computing-software.general-digital-literacy.file-management.reducing-pdf-file-size
name: reducing-pdf-file-size
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-scanning, compress-pdf, pdf-size, reduce-file-size]
level: intro
status: docs-checked
description: "Shrink a large PDF to fit email or upload limits with Mac Preview export options, check the Gmail attachment limit, and avoid uploading private documents to random sites."
sources:
  - https://support.apple.com/en-au/guide/preview/prvw1509/mac
  - https://support.google.com/mail/answer/6584
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reduce PDF file size

## Mac Preview
- Open the PDF, File > Export, set **Quartz Filter** to *Reduce File Size*, Save. Apple warns the result may be lower quality than the original.
- Other Export tick boxes: *Create Linearised PDF*, *Optimise images for screen*, *Save images as JPEG*.
- Save under a different filename to keep the original.

## Email limit
- Personal Gmail attachments: 25 MB total. Over the limit, Gmail adds the file as a Google Drive link instead.

## Privacy
- Free "compress PDF" websites receive whatever you upload. Prefer local tools for personal documents.

## Verify
- [ ] The new size meets the limit; zoom in and check small print is still legible.

## Checked
2026-11-01. Confirmed: Apple Preview User Guide "Reduce the size of a PDF" (Quartz Filter, export options, quality warning); Gmail Help "Send attachments" (25 MB personal limit, Drive link). Removed: Acrobat steps (page returned 404), Word and ColorSync steps, ppi/dpi targets, Ghostscript command, Outlook and portal limits, tool recommendations (no page read).
Method: documentation only; no commands were run.
