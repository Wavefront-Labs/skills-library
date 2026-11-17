---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.search-pipeline-processors
name: search-pipeline-processors
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, search-pipeline-processors, os-search-pipelines]
level: advanced
status: docs-checked
description: "Create request and response processors in an OpenSearch search pipeline and apply it per request or as an index default."
sources:
  - https://docs.opensearch.org/latest/search-plugins/search-pipelines/index/
  - https://docs.opensearch.org/latest/search-plugins/search-pipelines/creating-search-pipeline/
  - https://docs.opensearch.org/latest/search-plugins/search-pipelines/using-search-pipeline/
  - https://docs.opensearch.org/latest/search-plugins/search-pipelines/search-processors/
  - https://docs.opensearch.org/latest/search-plugins/search-pipelines/filter-query-processor/
  - https://docs.opensearch.org/latest/search-plugins/search-pipelines/rename-field-processor/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search pipelines (OpenSearch)

**Goal:** modify queries and results server-side. Search pipelines are an OpenSearch feature; the Elasticsearch pages used for this review do not document them.
- Create: `PUT /_search/pipeline/my_pipeline {"request_processors":[{"filter_query":{"tag":"tag1","query":{"term":{"visibility":"public"}}}}],"response_processors":[{"rename_field":{"field":"message","target_field":"notification"}}]}`. Pipelines are stored in the cluster state; processors run in the listed order, and the same processor type may appear more than once, so give each a `tag` to help debug errors.
- Processor kinds: request processors (intercept the search request), response processors (intercept the response), and search phase results processors (run between phases on the coordinating node, such as `normalization-processor`). Request and response processing both happen on the coordinating node; there is no shard-level processing.
- `filter_query` requires `query` (a Query DSL object). `rename_field` requires `field` and `target_field`.
- Use it per request: `GET /my_index/_search?search_pipeline=my_pipeline`, or `"search_pipeline": "my_pipeline"` in the body. A temporary pipeline can be defined inline under `search_pipeline` in the body and is not persisted.
- Default for an index: `PUT /my_index/_settings {"index.search.default_pipeline": "my_pipeline"}`. Bypass it for one request with `search_pipeline=_none`; remove it by setting the value to `null` or `_none`.
- By default a pipeline stops when a processor fails; set `"ignore_failure": true` on a processor to log the failure and continue. Replace a pipeline by sending `PUT` again; an optional `version` number is returned by `GET _search/pipeline/<id>`.
- Processor availability depends on the version: the documentation lists the earliest version of each (for example `filter_query` and `rename_field` 2.8, `oversample` 2.12, `normalization-processor` 2.10). List what a cluster supports with `GET /_nodes/search_pipelines`.

## Verify
- [ ] The response shows the renamed field and only the filtered results.

## Checked

2026-11-08. Confirmed against the OpenSearch search pipeline overview, creating, using, processor list, filter_query and rename_field pages. Removed the Elasticsearch documentation link (no search pipelines there), the example field names that differed from the docs, and the claim that a missing processor makes creation fail (the pages do not state it).
Method: documentation only; no commands were run.
