---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.ingest-pipeline-create
name: ingest-pipeline-create
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, ingest-pipeline-create, es-ingest-pipelines]
level: practitioner
status: docs-checked
description: "Define an ingest pipeline with processors and attach it with the pipeline parameter or the index.default_pipeline setting."
sources:
  - https://www.elastic.co/docs/manage-data/ingest/transform-enrich/ingest-pipelines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create and apply an ingest pipeline

**Goal:** transform documents before indexing.
```
PUT _ingest/pipeline/clean
{"processors":[{"lowercase":{"field":"user"}},{"set":{"field":"ingested","value":"{{{_ingest.timestamp}}}"}},{"remove":{"field":"tmp","ignore_missing":true}}]}
```
- A pipeline is an ordered list of processors plus optional `description` and integer `version` (usable with `if_version`). It is stored in cluster state.
- Per request: `POST my-index/_doc?pipeline=clean` (also bulk, reindex and update-by-query). Default: `"index.default_pipeline":"clean"` in settings; `index.final_pipeline` runs after the request or default pipeline even if neither is given.
- `_ingest.timestamp` exists by default but is not indexed unless a `set` processor copies it into a field.
- Documented common processors: `set` (Mustache templates), `lowercase`, `rename`, `dot_expander`, `split`, `pipeline`, `fail`, `drop`; processors can run conditionally with a Painless `if`.
- Test with the simulate API before attaching.
- Pipelines do not change already indexed documents; reindex or update-by-query to apply them.
- A pipeline stops at the first failing processor unless `ignore_failure` or `on_failure` is set.
- Nodes with the `ingest` role run pipelines; heavy workloads may need dedicated ingest nodes, and expensive regular expressions or complex `if` scripts slow indexing.
- Pipelines work on one document at a time; they cannot split a document into several.

## Verify
- [ ] Index a sample doc with `?pipeline=clean` and `GET` it back.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch ingest pipelines page in full; `remove` and `ignore_missing` in the example were not on the page. OpenSearch was not checked.
