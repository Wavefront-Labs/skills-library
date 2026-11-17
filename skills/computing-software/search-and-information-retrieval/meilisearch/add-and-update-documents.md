---
id: computing-software.search-and-information-retrieval.meilisearch.add-and-update-documents
name: add-and-update-documents
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [add-documents, partial-update, skip-creation, meilisearch]
level: practitioner
status: docs-checked
description: "Choose between Meilisearch POST (replace), PUT (merge) and delete document operations, use skipCreation, fetch by ID, and send JSON, NDJSON or CSV."
sources: ["https://www.meilisearch.com/docs/capabilities/indexing/how_to/add_and_update_documents"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add and update documents

| Operation | Call | Behaviour |
|---|---|---|
| Add or replace | `POST /indexes/<uid>/documents` | Replaces the whole document with the same primary key; omitted fields vanish |
| Add or update | `PUT /indexes/<uid>/documents` | Merges top-level fields; omitted fields stay |
| Delete | `DELETE /indexes/<uid>/documents/<id>` | Removes one document |

Partial updates are per top-level field: updating an object field replaces the entire object and drops omitted subfields. Example: replacing `{id: 287947, title, overview, genres}` with a body lacking `genres` removes `genres`, while a PUT with only `title` and `genres` keeps `overview`.

Batch deletion uses `POST .../documents/delete-batch` (array of IDs) and filter deletion `POST .../documents/delete`.

## Batching and skipCreation

Send arrays of documents; a batch is one task, so prefer bulk over one-at-a-time. Both POST and PUT create missing documents unless you add `?skipCreation=true`, which silently ignores documents whose primary key does not exist yet, avoiding incomplete records.

## Fetching

Prefer `POST /indexes/<uid>/documents/fetch` with `{"ids": [...]}` and/or a `filter` over the GET route (fewer parameters, string filters only). Results are unordered and unknown IDs are ignored. A fetch filter attribute must be in `filterableAttributes`.

## Content types

JSON array by default; NDJSON (`application/x-ndjson`) and CSV (`text/csv`) are accepted via the header. `csvDelimiter` (for example `;`) is valid only with `text/csv`.

## Checked

Method: docs-checked 2026-11-09 against the Add and update documents page (raw mdx of github.com/meilisearch/documentation, read in full). All claims confirmed.
