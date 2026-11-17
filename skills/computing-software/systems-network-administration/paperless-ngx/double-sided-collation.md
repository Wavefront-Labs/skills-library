---
id: computing-software.systems-network-administration.paperless-ngx.double-sided-collation
name: double-sided-collation
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, collate, double-sided, adf, single-sided-scanner, duplex]
level: practitioner
status: docs-checked
description: "Merge two single-sided ADF scans into one correctly ordered document with the double-sided collate feature."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collating double-sided scans

For scanners with a one-sided feeder. If your scanner does duplex, skip this.

## Enable
```bash
PAPERLESS_CONSUMER_RECURSIVE=true
PAPERLESS_CONSUMER_ENABLE_COLLATE_DOUBLE_SIDED=true
```
Optional: `PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_SUBDIR_NAME` (default `double-sided`) and `PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_TIFF_SUPPORT`. Create the subdirectory yourself; Paperless will not.

## Workflow
1. Scan the stack (pages 1, 3, 5) into the `double-sided` subfolder. It goes to internal staging.
2. Flip the stack without reordering and scan again (pages 6, 4, 2).
3. Paperless reverses the second scan, interleaves, and consumes pages 1 to 6 as one document.
You may omit trailing blank even pages, but never blank ones in the middle.

## Failure modes
- Odd scan with fewer pages than the even scan: both are discarded with an error; restart from the odd pages.
- Files must arrive in order and one at a time, with Paperless running. With polling, set `PAPERLESS_CONSUMER_POLLING_INTERVAL` below the gap between scans.
- A staged odd scan expires after 30 minutes.

## Combinations
- With subdirs as tags, `double-sided/foo/bar` and `foo/bar/double-sided` both give tags `foo` and `bar` but not `double-sided`.
- With barcode splitting, put the split barcode on both sides of the marker sheet, so the extra blank page is removed.

## Checked
2026-11-04. Compared with Automatic collation of double-sided documents in advanced usage and the Collate Double-Sided Documents settings in configuration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: required settings, defaults, directory not auto-created, workflow and page order, trailing blank page tip, failure modes, 30 minute expiry, polling interval, subdirs-as-tags and split barcode interactions. Nothing removed.

Method: documentation only; no commands were run.
