---
id: computing-software.systems-network-administration.paperless-ngx.barcode-splitting-asn
name: barcode-splitting-asn
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, barcodes, document-splitting, asn, patch-t, archive-serial-number]
level: advanced
status: docs-checked
description: "Enable barcode scanning to split batch scans on separator pages and set archive serial numbers from ASN labels."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/usage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Barcode splitting and ASN

Barcodes work for PDFs, and TIFFs when `PAPERLESS_CONSUMER_BARCODE_TIFF_SUPPORT=true`. Only the content matters, not the barcode type (QR, Code 128, EAN, Data Matrix, PDF417 and others are supported by the zxing-cpp backend).

## Splitting
Enable with `PAPERLESS_CONSUMER_ENABLE_BARCODES=true`. The default separator text is `PATCHT` (`PAPERLESS_CONSUMER_BARCODE_STRING`), the classic PATCH-T sheet.
- Default: a separator page ends a document, starts a new one on the next page, and is discarded.
- `PAPERLESS_CONSUMER_BARCODE_RETAIN_SPLIT_PAGES=true` keeps the page as the first page of the new document.
If no barcodes are found in the uploaded file, no split happens. When a file is split, the original is removed and the separated pages are saved as PDF. Barcode support for TIFFs converts them to PDFs for processing.

## ASN
`PAPERLESS_CONSUMER_ENABLE_ASN_BARCODE=true` reads values like `ASN00123` (prefix `PAPERLESS_CONSUMER_ASN_BARCODE_PREFIX`, default `ASN`; non-numeric characters after it are dropped). The ASN barcode page is kept and each one starts a new document. A barcode with an ASN that already exists makes the document fail with an error.

## Detection tuning
- `PAPERLESS_CONSUMER_BARCODE_DPI` default 300 (try 600) and `PAPERLESS_CONSUMER_BARCODE_UPSCALE` (above 1.0, for example 1.5) help with small barcodes.
- `PAPERLESS_CONSUMER_BARCODE_MAX_PAGES` default 0 scans all pages.

## v3
The pyzbar scanner and `CONSUMER_BARCODE_SCANNER` setting are removed; just delete the setting.

## Checked
2026-11-04. Compared with the Barcodes section of configuration, the Barcodes section of advanced_usage and the barcode scanner changes in the v3 migration page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: PDF and TIFF support, supported barcode types, enable and string settings with PATCHT default, split-after behaviour and the retain setting, ASN prefix and cleaning, existing-ASN failure, DPI 300, upscale above 1.0, max pages 0, removed scanner setting. Reworded the no-barcode sentence: the docs say the original is removed and pages saved as PDF when a split happens, not when none is found.

Method: documentation only; no commands were run.
