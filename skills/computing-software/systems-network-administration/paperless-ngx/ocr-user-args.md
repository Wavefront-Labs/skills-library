---
id: computing-software.systems-network-administration.paperless-ngx.ocr-user-args
name: ocr-user-args
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, ocr-user-args, ocrmypdf, unpaper, deskew, ocr-clean]
level: advanced
status: docs-checked
description: "Pass extra OCRmyPDF options safely with PAPERLESS_OCR_USER_ARGS and tune cleaning, deskew and rotation settings."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/troubleshooting/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCR tuning and user arguments

## Built-in knobs
- `PAPERLESS_OCR_CLEAN`: `clean` (default) runs unpaper before Tesseract; `clean-final` also uses the cleaned images to build the output; `none` skips unpaper. `clean-final` is incompatible with OCR mode `redo`, where `clean` is used instead.
- `PAPERLESS_OCR_DESKEW`: default true. Deskewing is disabled automatically when the OCR mode is `redo`.
- `PAPERLESS_OCR_ROTATE_PAGES`: default true, with `PAPERLESS_OCR_ROTATE_PAGES_THRESHOLD` default 12. A value of 15 is very conservative; 2 is very aggressive and often rotates correctly rotated pages too.
- `PAPERLESS_OCR_IMAGE_DPI`: fallback DPI for images that lack one. Unset means the DPI is calculated so the produced PDF is A4 sized.
- `PAPERLESS_OCR_MAX_IMAGE_PIXELS`: above the limit Paperless warns; above twice the limit it does not OCR the image (the document is still consumed). Unset uses the Pillow default; `0` disables the limit, which the docs warn against for documents that may be malicious.

## PAPERLESS_OCR_USER_ARGS
A JSON dictionary passed to the OCRmyPDF API. Use lower-case booleans, double-quoted names and strings, and underscores instead of dashes:
```json
{"deskew": true, "optimize": 3, "unpaper_args": "--pre-rotate 90"}
```
Many options conflict, and invalid options may prevent Paperless from consuming any documents. Only trusted users should change it, which includes anyone holding the `AppConfig` permission, because the arguments are passed directly to OCRmyPDF.

## Known fix
For the error "Ghostscript PDF/A rendering failed":
```bash
PAPERLESS_OCR_USER_ARGS='{"continue_on_soft_render_error": true}'
```

## Checked
Date: 2026-11-07
Pages read in full: configuration (docs/configuration.md), troubleshooting (docs/troubleshooting.md).
Corrections: replaced "Unset means the PDF is sized A4" with the documented DPI calculation; added the redo interactions and the documented Pillow default for the pixel limit; named the exact error string from troubleshooting.
Method: documentation only; no commands were run.
