---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.bulk-api-usage
name: bulk-api-usage
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, bulk-api-usage]
level: practitioner
status: docs-checked
description: "Send newline-delimited action and source pairs to _bulk, check per-item errors and retry only the failed items."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk
  - https://docs.opensearch.org/latest/api-reference/document-apis/bulk/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use the bulk API correctly

**Goal:** reliable high-throughput writes.
```
POST _bulk
{"index":{"_index":"my-index","_id":"1"}}
{"title":"a"}
{"delete":{"_index":"my-index","_id":"2"}}
```
- Body must be NDJSON: each action and source on its own line (not pretty printed), the final line ending in a newline, with `Content-Type: application/x-ndjson` (Elasticsearch also accepts `application/json`). Use `curl --data-binary`, not `-d`, which drops newlines.
- A delete action has no source line; `index` and `create` expect a source; `update` expects the partial doc, `upsert` or script on the next line.
- The response has a top-level `errors` flag and a per-item `status`: always check them and retry or log only the failed items. Client library bulk helpers can handle batching and retry.
- Batch size: OpenSearch suggests starting with 1,000 to 5,000 operations and a typical 5 MB to 15 MB per request; Elasticsearch says there is no correct number, to experiment, and that its default HTTP request limit is 100mb.
- `update` actions accept `retry_on_conflict` inside the action line.

## Verify
- [ ] Response `errors` is false, and `GET my-index/_count` equals the expected number.

## Checked
Date: 2026-11-07
- Elasticsearch bulk API page: read the introduction through the cURL notes (privileges, NDJSON layout, final-newline and Content-Type note, action semantics, size guidance, 100mb limit), plus searched the `retry_on_conflict` and error-response examples (`errors: true`, per-item `status`). The long parameter and response schema was not read in full.
- OpenSearch bulk API page: searched and read the NDJSON, `--data-binary`, `x-ndjson`, batch size (1,000 to 5,000 operations, 5 MB to 15 MB), `retry_on_conflict` and "always check the errors field" passages; not read end to end.
- Removed: the HTTP 429 and `es_rejected_execution_exception` claims, and "a few MB" batches; neither page mentions 429 or that exception string, so the thread-pool rejection guidance is unconfirmed here.
Method: documentation only; no commands were run.
