---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.data-stream-backing-indices
name: data-stream-backing-indices
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, data-stream-backing-indices]
level: advanced
status: docs-checked
description: "Understand hidden backing indices, naming, searching across them, and deleting or modifying them safely."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/data-streams
  - https://www.elastic.co/docs/manage-data/data-store/data-streams/modify-data-stream
  - https://www.elastic.co/docs/manage-data/data-store/data-streams/use-data-stream
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Work with backing indices

**Goal:** operate on generations without breaking the stream.
- A data stream consists of one or more hidden, auto-generated backing indices named `.ds-<data-stream>-<yyyy.MM.dd>-<generation>`; the generation is a six-digit zero-padded integer starting at `000001` and the date is the backing index's creation date. Do not derive meaning from the names: shrink or restore can rename a backing index, and some generations never exist.
- Search the stream name. New documents go only to the write index (the most recently created backing index); you cannot add documents to the other backing indices, and cannot clone, delete, shrink or split the write index.
- Mappings and settings come from the stream's index template: update the template so new backing indices get the change, and see the Modify a data stream page for changes to existing fields or static settings (a reindex is often required). Rolling over applies a new template setting to the write index straight away.
- Deleting a data stream deletes all its backing indices and their data.
- To update or delete a single document, send the request to the backing index that holds it.

## Verify
- [ ] The generations of the backing indices reported by `GET _data_stream/<name>` match the `.ds-` index names.

## Scope
The Elasticsearch documentation was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch docs pages Data streams, Modify a data stream and Use a data stream. Confirmed: all statements above. Removed: the `expand_wildcards=all` listing tip, "delete old data by deleting the older backing index" and `_cat/indices/.ds-*` (not stated on the pages read), and the OpenSearch source root.

Method: documentation only; no commands were run.
