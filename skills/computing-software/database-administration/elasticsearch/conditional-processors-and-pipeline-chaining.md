---
id: computing-software.database-administration.elasticsearch.conditional-processors-and-pipeline-chaining
name: conditional-processors-and-pipeline-chaining
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, conditional-processor, pipeline-processor, ingest-pipelines, painless, elasticsearch-ingest]
level: practitioner
status: verified
description: "Run Elasticsearch ingest processors conditionally with if (Painless), and split logic into reusable pipelines called with the pipeline processor."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html#conditionally-run-processor
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/pipeline-processor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional processors and pipeline chaining

## if conditions
Every processor accepts `if` (a Painless expression on `ctx`):
```json
PUT _ingest/pipeline/logs-main
{ "processors": [
  { "set": { "field": "event.kind", "value": "alert", "if": "ctx.log?.level == 'error'" } },
  { "drop": { "if": "ctx.url?.path != null && ctx.url.path.startsWith('/healthz')" } },
  { "pipeline": { "name": "logs-nginx", "if": "ctx.service?.type == 'nginx'" } },
  { "pipeline": { "name": "logs-java",  "if": "ctx.service?.type == 'java'", "ignore_missing_pipeline": true } }
] }
```
- Use the null-safe operator `?.`: a missing field otherwise throws a null pointer error and fails the document.
- Conditions are compiled scripts; keep them simple. `script.max_compilations_rate` (default `150/5m`) limits script compilations.
- `drop` discards the document silently; the `drop` processor's stats `count` is lower than the pipeline's `count` by the number dropped (2 documents in, 1 through the drop step); use it for noise.

## Chaining pipelines
- `pipeline` processor runs another pipeline inline, sharing `ctx`. Build small pipelines per source format and a router pipeline that dispatches.
- Recursion is detected and fails.
- Access the current pipeline name via `{{_ingest.pipeline}}` (a real indexed document got `pn: dp`).

## Tagging for debugging
Add `"tag": "nginx-grok"` to processors: tags appear in error messages and in `_ingest/pipeline/_simulate?verbose=true` output.

## Testing
```json
POST _ingest/pipeline/logs-main/_simulate?verbose=true
{ "docs": [ { "_source": { "service": { "type": "nginx" }, "message": "..." } } ] }
```
Verbose shows each processor's result, including skipped conditional ones.

## Verify
`GET _nodes/stats/ingest?filter_path=nodes.*.ingest.pipelines.logs-*` shows counts per pipeline: routed pipelines receive the expected share of documents and `failed` stays 0.
