---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.update-delete-by-query
name: update-delete-by-query
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, update-delete-by-query]
level: practitioner
status: docs-checked
description: "Modify or delete many documents matching a query in OpenSearch with conflicts handling, throttling, slicing and async task tracking."
sources:
  - https://docs.opensearch.org/latest/api-reference/document-apis/update-by-query/
  - https://docs.opensearch.org/latest/api-reference/document-apis/delete-by-query/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update by query and delete by query

**Goal:** bulk changes without a client loop.
- `POST my-index/_update_by_query?conflicts=proceed {"script":{"source":"ctx._source.flag = true","lang":"painless"},"query":{...}}`. With no body it updates every document, which re-indexes them to pick up mapping changes.
- `POST my-index/_delete_by_query {"query":{"range":{"@timestamp":{"lt":"now-90d"}}}}`.
- Both take a snapshot (a scroll context for delete) at the start and use internal versioning. A document that changes in between causes a version conflict for that document; `conflicts` is `abort` or `proceed`. Completed changes are not rolled back if later ones fail. Failures abort the operation and are listed in `failures`.
- Rejected search or bulk requests are retried up to 10 times with exponential backoff, then the operation halts and returns the failed requests.
- Scripts can set `ctx.op = "noop"` (counted in `noops`) or `ctx.op = "delete"` (counted in `deleted`); any other `ctx.op` value, or modifying `ctx` fields other than `ctx._source` and `ctx.op`, is an error.
- `wait_for_completion=false` returns a task ID and writes a task document at `.tasks/task/<TASK_ID>`; delete it after completion to reclaim space.
- `requests_per_second` throttles (`-1` disables; the page's default column shows 0); batch size defaults to 1,000 (`scroll_size` default is 100 in the update table). `slices=auto` runs in parallel: best query performance when slices equals shard count, and use fewer for indexes with 500 or more shards.
- `refresh` refreshes all shards involved when the request completes and does not accept `wait_for` for these two APIs.
- `max_docs` limits documents processed; `size` is deprecated in favour of it. Documents with version 0 cannot be updated.
- Gotcha: with `_source`, `_source_includes` or `_source_excludes` on update by query, excluded fields are not seen by the script and may be removed from the document unless the script restores them.

## Verify
- [ ] Run the same query as `_count` before and after to confirm the effect.

## Scope
OpenSearch pages checked. The Elasticsearch equivalents were not fetched. The old claim that delete-by-query space is only freed on segment merge is not on these pages and was removed.

## Checked

Checked 2026-11-08 against the OpenSearch Update By Query API and Delete By Query API pages. Confirmed: snapshot and versioning behaviour, conflicts values, retries, `ctx.op` rules, async task document, throttling, slicing guidance and refresh restriction. Removed: the merge and space-reclaim claim and the page-root sources.

Method: documentation only; no commands were run.
