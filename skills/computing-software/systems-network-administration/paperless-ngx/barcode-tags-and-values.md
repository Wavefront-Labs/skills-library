---
id: computing-software.systems-network-administration.paperless-ngx.barcode-tags-and-values
name: barcode-tags-and-values
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, tag-barcode, barcode-mapping, store-barcode-values, barcodes, tag-assignment]
level: advanced
status: docs-checked
description: "Assign or create tags from barcodes with a regex mapping, optionally split on them, and store and search all barcode contents."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/usage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag barcodes and stored barcode values

## Tag assignment
Enable `PAPERLESS_CONSUMER_ENABLE_TAG_BARCODE=true`. Barcode text must match a regex in `PAPERLESS_CONSUMER_TAG_BARCODE_MAPPING`, a JSON dictionary of regex to substitution. The default is:
```json
{"TAG:(.*)": "\\g<1>"}
```
so `TAG:invoice` assigns tag `invoice`. Examples: `{"T-J": "JOHN", "T-S": "SMITH"}` maps codes directly to tags. Missing tags are created, matching ignores case, and comma-separated barcode text is split into several tags.

## Splitting on tag barcodes
`PAPERLESS_CONSUMER_TAG_BARCODE_SPLIT=true` splits at tag barcode pages, like ASN barcodes. The barcode page is kept and each piece takes only its own tags. A six-page scan with `TAG:invoice` on page 3 and `TAG:receipt` on page 5 yields three documents: pages 1-2 untagged, 3-4 invoice, 5-6 receipt. It also needs the tag barcode setting on.

## Storing contents
`PAPERLESS_CONSUMER_STORE_BARCODE_VALUES=true` keeps every barcode with the document: shown on the Metadata tab, returned in the `barcodes` field of `/api/documents/{id}/metadata/`, and searchable:
```
barcodes.value:DE89370400440532013000
barcodes.format:qrcode
```
Only the first `PAPERLESS_CONSUMER_BARCODE_MAX_PAGES` pages are scanned, and reprocessing reads barcodes of existing documents. Each version keeps its own.

## Checked
2026-11-04. Compared with the Barcodes section of configuration, the Tag Assignment, tag splitting and Barcode Contents parts of advanced_usage, and Searching barcodes in usage (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: default mapping, the T-J/T-S example, tag creation, case-insensitive matching, comma splitting, split behaviour and the six-page example, the dependency on the tag barcode setting, stored values on the Metadata tab and API field, the barcodes.value and barcodes.format search syntax, max pages, reprocessing, per-version barcodes. Nothing removed.

Method: documentation only; no commands were run.
