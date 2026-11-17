---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.update-and-upsert-documents
name: update-and-upsert-documents
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, update-and-upsert-documents]
level: practitioner
status: docs-checked
description: "Update documents with the _update API using doc, script, doc_as_upsert and detect_noop behaviour."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/rest-apis/update-document
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial update, scripted update and upsert

**Goal:** modify fields without resending whole documents.
- `POST my-index/_update/1 {"doc":{"status":"done"}}`; an update that changes nothing is detected and returns `"result": "noop"` (disable with `"detect_noop": false`).
- Script: `{"script":{"source":"ctx._source.count += params.n","params":{"n":1}}}`. A script can also set `ctx.op` to `delete` or `noop`.
- Upsert: either a partial `doc` plus an `upsert` document, or `{"doc":{...},"doc_as_upsert":true}`, which uses the `doc` as the upsert. `scripted_upsert: true` runs the script whether or not the document exists.

## Verify
- [ ] `GET my-index/_doc/1` shows the changed field.

## Scope
The Elasticsearch reference page was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference page Update a document. Confirmed: `doc`, scripts with `ctx._source` and `params`, `ctx.op`, noop detection and `detect_noop`, `upsert`, `doc_as_upsert`, `scripted_upsert`. Removed: "updates reindex the whole document / segments are immutable", "frequent updates of large documents are expensive" and the `_version` bump check (none stated on the page), and the OpenSearch source root.

Method: documentation only; no commands were run.
