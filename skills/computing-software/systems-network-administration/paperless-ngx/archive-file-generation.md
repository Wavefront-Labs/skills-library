---
id: computing-software.systems-network-administration.paperless-ngx.archive-file-generation
name: archive-file-generation
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, archive-file, pdfa, paperless-archive-file-generation, ocr-output-type, disk-space]
level: practitioner
status: docs-checked
description: "Control PDF/A archive creation with PAPERLESS_ARCHIVE_FILE_GENERATION (auto, always, never) and choose the PDF/A output level."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/usage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Archive file generation

Paperless always keeps the original untouched. An archive is a PDF/A copy stored alongside the original and used for display in the web interface.

## PAPERLESS_ARCHIVE_FILE_GENERATION
- `auto` (default): archives for scanned or image-based documents; skipped for born-digital PDFs that already carry text.
- `always`: an archive whenever the parser supports it, even for PDFs with text.
- `never`: originals only. Saves disk space; the viewer shows the original file.

Plain text, email and HTML never get an archive. Office files via Tika always get a PDF rendition, regardless of the setting. The remote OCR (Azure) parser honours the setting too: if no archive is wanted, the remote engine is skipped and locally extracted text is used, avoiding an API call.

## Output type
`PAPERLESS_OCR_OUTPUT_TYPE` accepts `pdf` (minimal changes), `pdfa` (default, PDF/A-2b) or `pdfa-1`, `pdfa-2`, `pdfa-3`.

## Failures
Ghostscript errors such as "PDF/A rendering failed" can be forced past with `PAPERLESS_OCR_USER_ARGS='{"continue_on_soft_render_error": true}'`. `PAPERLESS_OCR_COLOR_CONVERSION_STRATEGY` (CMYK, Gray, LeaveColorUnchanged, RGB, UseDeviceIndependentColor) can also cause archive errors.

## Rebuilding
`document_archiver` recreates missing archives; with `--overwrite` it redoes existing ones.

## Checked
2026-11-04. Compared with PAPERLESS_ARCHIVE_FILE_GENERATION, PAPERLESS_OCR_OUTPUT_TYPE and PAPERLESS_OCR_COLOR_CONVERSION_STRATEGY in configuration, the Ghostscript entry in troubleshooting and the document_archiver section of administration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: three modes and the default, file-type behaviour including Tika and the remote OCR note, output types and PDF/A-2b default, the continue_on_soft_render_error setting, colour strategy options, document_archiver and --overwrite. Reworded the opening sentence to the docs' wording (dropped "text layer for scans").

Method: documentation only; no commands were run.
