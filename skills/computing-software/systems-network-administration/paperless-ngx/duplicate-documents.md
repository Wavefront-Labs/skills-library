---
id: computing-software.systems-network-administration.paperless-ngx.duplicate-documents
name: duplicate-documents
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, duplicates, consumer-delete-duplicates, checksum, fuzzy-match, document-fuzzy-match]
level: practitioner
status: docs-checked
description: "Understand how v3 treats duplicates, find them in the UI and API, reject them at consumption, and detect near-duplicates with document_fuzzy_match."
sources:
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/administration/"
  - "https://docs.paperless-ngx.com/faq/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duplicate documents

## Default behaviour in v3
Duplicates are not rejected. A file whose original or archive checksum matches an existing document is consumed anyway and a warning is logged. The document gets a Duplicates tab listing visible documents with the same content, including ones in the trash.

## Finding them
- Document list text filter: choose Duplicates.
- API: `has_duplicates=true`.

## Rejecting at consumption
Set `PAPERLESS_CONSUMER_DELETE_DUPLICATES=true` for the pre-v3 behaviour: the duplicate file is deleted and the task fails with "Document already exists", linking the original.

## Near-duplicates
A fresh scan is rarely bit-identical. The management command compares content:
```bash
document_fuzzy_match --ratio 85 --processes 2
```
- `--ratio` (default 85.0, range 0 to 100) is the similarity threshold.
- `--processes` defaults to a quarter of the cores; 1 disables multiprocessing.
- `--url <INSTANCE_URL>` prints links instead of IDs.
- `--delete` removes one of each matching pair; take a backup first.
- Other metadata such as correspondent is not considered.

## Script caution
A pre-consume script that changes the working file in a non-deterministic way can let duplicates through.

## Checked
2026-11-04. Compared with Duplicate documents in usage, PAPERLESS_CONSUMER_DELETE_DUPLICATES in configuration, Detecting duplicates in administration, and the pre-consume script warning in advanced usage (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: v3 default, Duplicates tab and trash note, filter and has_duplicates, reject-on-consume behaviour, document_fuzzy_match options and defaults, metadata not considered, script caution. Nothing removed.

Method: documentation only; no commands were run.
