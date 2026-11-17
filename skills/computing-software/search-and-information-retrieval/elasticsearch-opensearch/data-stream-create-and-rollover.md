---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.data-stream-create-and-rollover
name: data-stream-create-and-rollover
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, data-stream-create-and-rollover, es-data-streams]
level: practitioner
status: docs-checked
description: "Create an index template with data_stream, write to the stream, and roll over the write index manually or by lifecycle."
sources:
  - https://www.elastic.co/docs/manage-data/data-store/data-streams
  - https://www.elastic.co/docs/manage-data/data-store/data-streams/set-up-data-stream
  - https://www.elastic.co/docs/manage-data/data-store/data-streams/use-data-stream
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a data stream and roll it over

**Goal:** append-only time series data with automatic backing indices.
- The index template must be data-stream enabled (`"data_stream":{}`), have index patterns matching the stream name, and use a priority higher than `200` to avoid collisions with built-in templates (built-ins have priority `100`, Fleet templates up to `200`; for an overlapping pattern such as `logs-*` the Templates page suggests above `500`): `PUT _index_template/logs-ds {"index_patterns":["logs-app-*"],"data_stream":{},"priority":501}`.
- Every document needs a `@timestamp` field (mapped `date` or `date_nanos`; if the template does not map it, Elasticsearch maps it as `date`).
- Indexing requests must use an `op_type` of `create` (bulk `create` actions). An indexing request that targets a name matching a template's index pattern creates the data stream automatically.
- Manual rollover: `POST logs-app-prod/_rollover`; a rollover creates a new backing index that becomes the write index. ILM is recommended for automatic rollover.
- Inspect: `GET _data_stream/logs-app-prod`.
- You cannot send update or delete requests for existing documents directly to a data stream; update or delete in the document's backing index, or use update by query / delete by query on the stream.
- Deleting a data stream also deletes its backing indices and data; you cannot delete an index template in use by a data stream.

## Verify
- [ ] After rollover `GET _data_stream/logs-app-prod` lists a new backing index (higher generation).

## Scope
The Elasticsearch documentation was checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch docs pages Data streams, Set up a data stream and Use a data stream. Confirmed: all statements above. Removed: explicit `PUT _data_stream/<name>` creation (not shown in the pages read; automatic creation is documented), the claim that documents without `@timestamp` are "rejected" (the pages say every document must contain it), and the OpenSearch source root.

Method: documentation only; no commands were run.
