---
id: computing-software.systems-network-administration.paperless-ngx.ocr-mode
name: ocr-mode
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, ocr, paperless-ocr-mode, ocrmypdf, tesseract, skip-text]
level: practitioner
status: docs-checked
description: "Choose PAPERLESS_OCR_MODE (auto, redo, force, off) and migrate old skip and skip_noarchive values to the v3 equivalents."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCR mode

`PAPERLESS_OCR_MODE` controls when and how OCR runs; archive creation is a separate setting (`PAPERLESS_ARCHIVE_FILE_GENERATION`).

- `auto` (default): detects embedded text with pdftotext. If sufficient text is found, OCR is skipped for that document (`--skip-text`); otherwise OCR runs normally. The safest option for mixed collections.
- `redo`: OCRs all pages and attempts to replace existing text layers. Useful for scanners whose own OCR had insufficient results; it also OCRs purely digital documents. It may fail on documents with features that cannot be removed, such as forms, in which case the document's existing text is used.
- `force`: rasterises documents, converting text to images and putting the OCRed text on top. Works for all documents, but the result may be significantly larger and text will not look as sharp when zoomed in.
- `off`: never invokes the OCR engine. PDFs get text via pdftotext only; image documents get empty text. Archive generation still works via format conversion.

## Interactions
- `PAPERLESS_OCR_CLEAN=clean-final` is incompatible with `redo`; `clean` is used instead.
- Deskewing is disabled automatically when the mode is `redo`.
- `PAPERLESS_OCR_PAGES=1` limits OCR to the first page; with `redo` or `force`, text on excluded pages is copied verbatim rather than modified.

## v3 migration
- `PAPERLESS_OCR_MODE=skip` becomes `auto` plus `PAPERLESS_ARCHIVE_FILE_GENERATION=always` (to keep v2's always-archive behaviour).
- `skip_noarchive` becomes `auto` plus `PAPERLESS_ARCHIVE_FILE_GENERATION=never`.
- `PAPERLESS_OCR_SKIP_ARCHIVE_FILE` is removed (`never` maps to generation `always`, `with_text` to `auto`, `always` to `never`).

A startup warning is logged if a removed variable is still set. Values you changed in the admin UI (ApplicationConfiguration) are migrated automatically; review them afterwards, and users who relied on the old defaults must set `archive_file_generation` to `always` to keep always creating an archive.

## Checked
Date: 2026-11-07
Pages read in full: configuration (docs/configuration.md), migration-v3 (docs/migration-v3.md).
Corrections: added the missing mapping for `PAPERLESS_OCR_SKIP_ARCHIVE_FILE` values and the old-defaults caveat from the migration page; tightened each mode description to the configuration text.
Method: documentation only; no commands were run.
