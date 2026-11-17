---
id: computing-software.cybersecurity-defensive.suricata.file-extraction-and-file-keywords
name: file-extraction-and-file-keywords
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [filestore, file-extraction, filemagic, filesha256]
level: practitioner
status: docs-checked
description: "Extract files with the filestore keyword and file-store output; match with fileext, filemagic and hash lists; set stream-depth and body limits."
sources: ["https://docs.suricata.io/en/latest/file-extraction/file-extraction.html", "https://docs.suricata.io/en/latest/rules/differences-from-snort.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# File extraction

Works over HTTP, SMTP, FTP, NFS, SMB and HTTP2 parsers; no rules means no extraction.

## Keywords
- `filestore`: store matching files (alone it stores all).
- `fileext`: claimed extension. `filemagic`: detected type.
- `filemd5`, `filesha1`, `filesha256`: match against a checksum list.

## Output
- `eve.files` writes metadata only; enable it under eve-log types (example: `force-magic: no`, `force-hash` md5 and sha256).
- `file-store` writes content, named by SHA256 under subdirectories 00 to ff, de-duplicated automatically. Only version 2 is documented.

## Limits
- `file-store.stream-depth` default 1 MB, 0 unlimited; it overrides `stream.reassembly.depth` for filestore and cannot be set lower.
- libhtp `request-body-limit` and `response-body-limit`; 0 is unlimited.
- `stream.checksum_validation` is on by default; offloading can make valid packets look bad.

## Checked

2026-11-04. Confirmed against the File Extraction page (protocols, settings, eve.files, file-store layout, stream-depth rules, rule keywords) and Differences From Snort (file keyword list).

Method: documentation only; no commands were run.
