---
id: computing-software.database-administration.elasticsearch.ingest-pipeline-failure-handling
name: ingest-pipeline-failure-handling
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, opensearch, ingest-pipeline, on-failure, ignore-failure, failure-store, dead-letter-index, pipeline-errors, ingest-metadata]
level: practitioner
status: verified
description: "Keep bad documents from being dropped by Elasticsearch ingest pipelines: processor and pipeline on_failure handlers, ignore_failure, dead-letter indices and failure stores."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html#handling-pipeline-failures
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/failure-store.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling ingest pipeline failures

**Goal:** a log line the pipeline cannot parse is kept and flagged, not rejected
and lost.

## Default behaviour
If any processor throws, the whole document is **rejected** with an error to the
client.

## Processor-level handling
```json
{ "grok": { "field": "message", "patterns": ["..."],
    "on_failure": [ { "set": { "field": "parse_error", "value": "{{ _ingest.on_failure_message }}" } } ] } },
{ "convert": { "field": "http.status", "type": "integer", "ignore_failure": true } },
{ "remove": { "field": "tmp", "ignore_missing": true } }
```
`ignore_failure` skips the processor silently; use for genuinely optional steps.
`ignore_missing` for absent fields.

## Pipeline-level: route to a dead-letter index
```json
PUT _ingest/pipeline/app-logs
{
  "processors": [ ... ],
  "on_failure": [
    { "set": { "field": "error.message", "value": "{{ _ingest.on_failure_message }}" } },
    { "set": { "field": "error.processor", "value": "{{ _ingest.on_failure_processor_type }}" } },
    { "set": { "field": "_index", "value": "failed-{{ _index }}" } }
  ]
}
```
The document is indexed into `failed-logs-app...` with the original message and
the error, so it can be fixed and reindexed. Give the failed index a permissive
mapping (or `"dynamic": false`) so it never rejects.

## Failure store (recent 8.x/9.x data streams; check your version's docs)
Data streams can enable a failure store: documents failing ingest or mapping are
stored in a `::failures` component automatically (`data_stream_options.failure_store.enabled: true`
in the index template). Prefer this on versions that support it.

## Monitor
```json
GET _nodes/stats/ingest?filter_path=nodes.*.ingest.pipelines.app-logs
```
`failed` counts per pipeline and per processor; alert when it rises, and on the
dead-letter index doc count.

## Gotchas
- Mapping conflicts happen after the pipeline (at indexing): on_failure doesn't catch them; the failure store does.
- A `fail` processor deliberately rejects; use it only when rejection is wanted.

## Verify
Send a deliberately malformed line: it appears in the failure index with
`error.message`, and the client receives a success response.
