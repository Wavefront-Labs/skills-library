---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.simulate-pipeline
name: simulate-pipeline
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, simulate-pipeline]
level: practitioner
status: docs-checked
description: "Test pipelines with the simulate API and verbose output before sending real traffic."
sources:
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-simulate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Simulate and debug a pipeline

**Goal:** see each processor's effect. Facts below are from the Elasticsearch API reference; check the OpenSearch
documentation for your version before relying on them there.
- Stored pipeline: `POST _ingest/pipeline/clean/_simulate {"docs":[{"_source":{"user":"BOB"}}]}`. The `id` path
  parameter names the pipeline to test.
- Inline definition: `POST _ingest/pipeline/_simulate {"pipeline":{...},"docs":[...]}`. If you give both the path
  `id` and a body `pipeline`, only the path `id` is used.
- `docs` is required; each entry needs `_source` and may carry `_id` and `_index`.
- Add `?verbose` (boolean, default false) to include output data for each processor in the response.
- The operation requires the `read_pipeline` cluster privilege.

## Verify
- [ ] Verbose simulate output ends with the expected `_source`.
- [ ] With `?verbose`, the response includes output data for each processor.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions.

## Checked
Checked against the Elasticsearch "Simulate a pipeline" API reference: the four method and path forms, `verbose`,
the required `docs` array with `_source`, the inline `pipeline` body and its precedence rule, and the privilege.
Removed unconfirmed claims: the `GET _ingest/pipeline/clean` and `GET _nodes/stats/ingest` tips, the statement that
simulate does not index so mapping conflicts only appear on a real index, and the OpenSearch landing page source.

Method: docs-only read of cited pages, 2026-11-08
