---
id: computing-software.digital-privacy-hygiene.privacy-configuration.properly-redacting-pdfs
name: properly-redacting-pdfs
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, pdf-redaction, redaction, metadata, acrobat, dangerzone, document-sanitization]
level: practitioner
status: docs-checked
description: "Redact PDFs so the content is removed, not just covered: Acrobat Redact then sanitise, Dangerzone pixel conversion, and why ExifTool cannot clean PDF metadata."
sources:
  - "https://helpx.adobe.com/acrobat/desktop/protect-documents/redact-pdfs/redact.html"
  - "https://dangerzone.rocks/"
  - "https://www.privacyguides.org/en/data-redaction/"
  - "https://exiftool.org/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Properly redacting PDFs

**Goal:** what you redact is gone from the file, not merely hidden under a rectangle.

## Methods that remove content
- **Adobe Acrobat Pro** (Adobe's Redact help page): All tools > Redact a PDF > **Redact text and images**, drag over
  the text or image, then **Apply**. In the dialog that opens, turn on the toggle to **sanitise and remove hidden
  information**, choose Continue, and save with a new name in the Save Sanitized Document dialog. Do not skip the
  sanitise toggle.
- **Dangerzone** (free, open source, maintained by the Freedom of the Press Foundation): converts a document to a PDF
  inside a sandbox with no network access, turns it into raw pixel data for each page, then rebuilds a PDF from the
  pixels. It supports more than 20 file types. It is built to neutralise malware, and the pixel round trip also means
  the output carries no text layer, so run your redaction first and treat Dangerzone as a final flattening step.
  Check the output yourself.

## Image and metadata traps
- Never use blur to redact text in an image; draw a box over it (Privacy Guides).
- Image thumbnails can expose original detail from cropped or erased areas, and Windows' built-in metadata remover does
  not remove many document items: comments, author names, tracked changes, hidden worksheets, slide notes, custom XML
  and revision histories (Privacy Guides). Remove these in the source document before exporting.
- ExifTool lists PDF as a supported format, but its documentation says changes to PDF files are reversible because the
  original metadata is never actually deleted. Do not rely on `exiftool -all=` to clean a PDF; use Acrobat's sanitise
  option or Dangerzone.

## Verify
- [ ] In a viewer, select all, copy and paste into a text editor: no redacted text appears.
- [ ] Open the saved file's properties and comments panel: no unexpected author, comments or attachments.
- [ ] The file you share is the new sanitised file, not the original.

## Checked
Checked 2026-11-08 against Adobe's "Redact sensitive content in Acrobat Pro" page, the Dangerzone home page, Privacy
Guides' data and metadata redaction page and the ExifTool home page. Removed: the poppler and img2pdf rasterising
commands, `pdftotext` check, the `exiftool -all:all= -overwrite_original` plus `qpdf --linearize` metadata step
(contradicted by ExifTool's note that PDF changes are reversible), the macOS Preview Redact claim, and unlisted Acrobat
menu names, none of which the cited pages support.
Method: docs-only read of cited pages, 2026-11-08
