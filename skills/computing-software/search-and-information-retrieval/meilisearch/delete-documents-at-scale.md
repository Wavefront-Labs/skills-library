---
id: computing-software.search-and-information-retrieval.meilisearch.delete-documents-at-scale
name: delete-documents-at-scale
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [delete-by-filter, delete-batch, document-lifecycle, meilisearch]
level: practitioner
status: docs-checked
description: "Remove many Meilisearch documents by filter, ID batch or full wipe, track deletedDocuments in the task, and plan expiry cleanups with filterable fields."
sources: ["https://www.meilisearch.com/docs/capabilities/indexing/how_to/delete_documents_at_scale"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delete documents at scale

## Strategies

- Delete by filter: `POST /indexes/<uid>/documents/delete` with `{"filter": "status = 'archived'"}`. Best for sets sharing an attribute. The filter attribute must be in `filterableAttributes` or the request errors. Such tasks cannot be autobatched, so each is its own batch; many of them mixed with other writes can slow the queue.
- Delete by IDs: `POST /indexes/<uid>/documents/delete-batch` with an array. Split very large lists into several requests, each its own task processed sequentially.
- Delete everything: `DELETE /indexes/<uid>/documents` keeps settings.

Filter examples: `expires_at < 1704067200`, `status = 'draft' AND updated_at < 1672531200`.

## Tracking

Deletion is asynchronous. The response gives a `taskUid` with `type: documentDeletion`. Fetch `GET /tasks/<uid>`; a succeeded task's `details` has `providedIds`, `deletedDocuments` and `originalFilter`.

## Lifecycle cleanup

If data expires, store a timestamp or status field, add it to `filterableAttributes` (PATCH settings), and schedule a job posting a delete-by-filter such as `expires_at < <now epoch>`.

## Checked

2026-11-03. Confirmed claim by claim against the Delete documents at scale page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: an unsupported nightly-sync use for delete-all.

Method: documentation only; no commands were run.
