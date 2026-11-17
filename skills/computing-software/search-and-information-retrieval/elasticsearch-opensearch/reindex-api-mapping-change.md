---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.reindex-api-mapping-change
name: reindex-api-mapping-change
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, reindex-api-mapping-change]
level: advanced
status: docs-checked
description: "Copy documents into a new index with the reindex API to change mappings or settings, with async runs, slices, throttling and conflicts handling."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reindex-indices
  - https://docs.opensearch.org/latest/api-reference/document-apis/reindex/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reindex into a new index

**Goal:** apply a mapping change that cannot be done in place.
- Create the destination index with the final mapping, shards and replicas first: the reindex does not copy settings, mappings or shard configuration (OpenSearch page). Then run `POST _reindex?wait_for_completion=false` with `{"source":{"index":"old"},"dest":{"index":"new"}}`; that returns a task ID.
- Prefer async for long runs: a synchronous request keeps the client waiting and will likely hit transport timeouts, though the reindex continues as a task (Elasticsearch page).
- Speed: `?slices=auto` (Elasticsearch: one slice per shard up to a limit; OpenSearch: default is 1, no slicing). Query performance is best when slices equals the shard count; more slices than shards adds overhead.
- Throttle: `requests_per_second` (any positive decimal; `-1` disables, the default). Change it on a running reindex with `POST _reindex/<TASK_ID>/_rethrottle?requests_per_second=100`; speeding up takes effect immediately, slowing down after the current batch.
- Track and cancel: `GET _tasks/<TASK_ID>` and `POST _tasks/<TASK_ID>/_cancel` (the OpenSearch page shows the cancel call and `GET /_tasks?actions=*reindex*`).
- Conflicts: `conflicts` is `abort` (default) or `proceed` (OpenSearch). `dest.op_type` is `index` (default; overwrites same-ID documents) or `create` (only new documents; required for data streams in OpenSearch).
- Reshaping while copying: a `script` can rename fields (`ctx._source.tag = ctx._source.remove("flag")`) or change `_index`; `_source` filtering copies a subset of fields; `dest.pipeline` runs an ingest pipeline.
- Multiple sources in one request: ID collisions are not handled and the last write wins in no reliable order; reindex indices one at a time so you can resume.
- Failure mode: reindex extracts and re-indexes `_source`, so it fails when `_source` is disabled (OpenSearch page) and drops anything not in `_source`.
- For a large copy the OpenSearch page suggests temporarily setting the destination `number_of_replicas` to 0 and restoring it afterwards.

## Verify
- [ ] `GET old/_count` equals `GET new/_count` before switching the alias.

## Checked

Checked 2026-11-08 against the Elasticsearch Reindex indices examples page and the OpenSearch Reindex Documents API page. Confirmed: every parameter, default and warning above. Removed: the `refresh` interval of -1 tip (not on either page) and the page-root sources.

Method: documentation only; no commands were run.
