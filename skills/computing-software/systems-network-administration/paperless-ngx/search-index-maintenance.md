---
id: computing-software.systems-network-administration.paperless-ngx.search-index-maintenance
name: search-index-maintenance
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, document-index, reindex, search-language, tantivy, index-task]
level: practitioner
status: docs-checked
description: "Rebuild or repair the Paperless-ngx search index with document_index, and know when Docker does it automatically."
sources:
  - "https://docs.paperless-ngx.com/administration/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search index maintenance

The index updates automatically whenever documents are added, changed or removed. If search yields non-existing documents or finds nothing, recreate it manually:
```
document_index {reindex,optimize} [--recreate] [--if-needed]
```
- `reindex` rebuilds the index from all documents in the database. This may take some time.
- `--recreate` wipes the existing index before rebuilding; use it when the index is corrupted or you want a fully clean rebuild.
- `--if-needed` skips the rebuild if the index is up to date (schema version, schema fingerprint and search language all match). Safe to run on every startup or upgrade.
- `optimize` is deprecated and a no-op; Tantivy manages segment merging automatically.

## Docker versus bare metal
Docker: on every startup the container runs `document_index reindex --if-needed`, so schema changes, language changes and missing indexes are rebuilt before the webserver starts; no manual step is required.

Bare metal: run this after each upgrade and after changing `PAPERLESS_SEARCH_LANGUAGE`; it is a no-op if the index is current:
```bash
cd src
python3 manage.py document_index reindex --if-needed
```

## Related settings
- `PAPERLESS_SEARCH_LANGUAGE`: stemmer language for the search index. Use an ISO 639-1 code (`en`, `de`) or a lowercase full name (`english`); capitalised Tantivy enum names are not valid. An invalid value raises an error at startup. Changing it rebuilds the index automatically on next startup. If unset it is inferred from `PAPERLESS_OCR_LANGUAGE`, and stemming is disabled if that language has no Tantivy stemmer.
- `PAPERLESS_INDEX_TASK_CRON`: scheduled search index update, default `0 0 * * *` (daily at midnight); the string `disable` stops automatic updates.
- v3 replaced the Whoosh search backend with Tantivy. The old index format is incompatible, so the index is rebuilt automatically on first startup after upgrading.

## Checked
Date: 2026-11-07
Pages read in full: none in full. I read the relevant sections of administration (Managing the document search index), configuration (PAPERLESS_INDEX_TASK_CRON and PAPERLESS_SEARCH_LANGUAGE entries) and migration-v3 (the Search Index section).
Corrections: removed the separate three-command code block in favour of the page's usage line; removed the unconfirmed closing sentence about running management commands with `--help` through `docker compose exec`; changed "invalid values stop startup" to the page's "raises an error at startup"; added the inference and stemming-disabled behaviour.
Method: documentation only; no commands were run.
