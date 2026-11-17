---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.ingest-failure-handling
name: ingest-failure-handling
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, ingest-failure-handling]
level: advanced
status: docs-checked
description: "Use on_failure, ignore_failure and the fail processor to route errors to a failed-document index rather than losing documents."
sources:
  - https://www.elastic.co/docs/manage-data/ingest/transform-enrich/ingest-pipelines
  - https://www.elastic.co/docs/reference/enrich-processor/fail-processor
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ingest failure handling

**Goal:** controlled behaviour when a processor fails.
- By default the pipeline stops at the first processor failure.
- Per processor: `"ignore_failure":true` runs the remaining processors; or `"on_failure":[{"set":{"field":"error","value":"{{{ _ingest.on_failure_message }}}"}}]` runs a handler list right after the failure, then the pipeline continues. Lists can be nested.
- Pipeline level: a failing processor with no `on_failure` of its own falls back to the pipeline's top-level `on_failure`, and the remaining processors do not run. Example: `"on_failure":[{"set":{"field":"_index","value":"failed-{{{ _index }}}"}}]` reroutes to a failed-index.
- Failure metadata `on_failure_message`, `on_failure_processor_type`, `on_failure_processor_tag`, `on_failure_pipeline` is readable only inside an `on_failure` block.
- The `fail` processor (required `message`, templated) raises an error on purpose, for example when a condition says the document should not pass.
- Bulk responses can partially fail: a top-level `errors:true` means at least one item failed; each failed item has an `error` object (`type`, `reason`) and other items still run. The client must check items and retry them; `filter_path=items.*.error` returns only the errors.
- Failure mode: swallowing errors silently with `ignore_failure` hides data quality problems; record the error in a field instead.

## Verify
- [ ] A deliberately bad document lands in the failed index with the error message set.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch ingest pipelines page (failure handling section) and fail processor page in full; the bulk API response section was read for the errors flag and per-item error only. OpenSearch was not checked.
