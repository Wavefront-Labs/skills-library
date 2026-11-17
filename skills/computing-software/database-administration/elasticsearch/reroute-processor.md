---
id: computing-software.database-administration.elasticsearch.reroute-processor
name: reroute-processor
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, reroute-processor, data-streams, ingest-pipelines, routing, elasticsearch-ingest]
level: practitioner
status: docs-checked
description: "Route documents to a different data stream at ingest with the Elasticsearch reroute processor (8.8+), using dataset and namespace from fields, plus permission and pipeline rules."
sources:
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/ingest-processor/reroute-processor.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reroute processor

**Goal:** a single ingest endpoint (`logs-generic-default`) where documents are routed to `logs-nginx-prod`, `logs-java-dev`, etc. based on their content, so each dataset gets its own mappings, ILM and permissions.

## Example
```json
PUT _ingest/pipeline/logs-router
{ "processors": [
  { "reroute": { "if": "ctx.service?.type == 'nginx'", "dataset": "nginx", "namespace": "{{service.environment}}" } },
  { "reroute": { "dataset": ["{{data_stream.dataset}}", "generic"], "namespace": ["{{data_stream.namespace}}", "default"] } }
] }
```
- Target naming follows `<type>-<dataset>-<namespace>`; `type` stays the same as the source stream (`logs`).
- `dataset` and `namespace` default to the document's current `data_stream.dataset` and `data_stream.namespace`; they accept field references or static values, and a list gives fallbacks when a field is null or missing. `dataset` cannot contain `-`.
- Alternatively `destination: "logs-special-prod"` sets the full name (it cannot be combined with `dataset`/`namespace`).
- After reroute, the remaining processors of the current pipeline (including the final pipeline) are skipped, and the document goes through the ingest pipeline of the new target. The processor also updates `data_stream.*` fields and `event.dataset` if present.

## Requirements
- Data stream mode requires data streams that follow the `<type>-<dataset>-<namespace>` naming scheme; the `type` cannot be changed. An index template must match the target so it is created correctly.
- The writing user or API key needs privileges on the final target (for example `auto_configure` or `create_index` to auto-create it), not just the source; otherwise the document is rejected with a security exception.

## Gotchas
- Routing cycles are detected automatically: a document routed back to a target it already passed through fails with an exception.
- Dataset/namespace cardinality explodes if derived from free-form fields: each value creates a data stream with its own shards.

## Verify
Index sample docs into the source stream; `GET _data_stream/logs-nginx-*` shows the target stream created and `GET logs-nginx-prod/_count` increases.

## Checked

Checked 2026-10-25 against elastic/elasticsearch `main` docs (Stack 9.x). Confirmed: data stream mode versus `destination` mode, defaults of `dataset` and `namespace`, fallback lists, `-` restriction, type cannot change, processors skipped after reroute, target pipeline runs, cycle detection, permissions on the final target. Removed the unconfirmed "invalid characters are sanitised" and the specific privilege pair claim (`create_doc`). The Elastic Agent integration routing note and the cardinality warning are not quoted from the docs; the cardinality advice is a design judgement.

Method: documentation only; no commands were run.
