---
id: computing-software.database-administration.elasticsearch.data-streams-and-index-templates
name: data-streams-and-index-templates
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, ingest-pipeline, data-stream, index-template, component-template, rollover, timestamp]
level: practitioner
status: verified
description: "Set up Elasticsearch data streams for append-only time series: component and composable index templates, backing indices, rollover, and how updates and deletes differ."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/data-streams.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-a-data-stream.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data streams and index templates

A **data stream** is a named, append-only target for time-stamped documents (logs, metrics,
events) backed by hidden indices `.ds-<name>-<date>-<generation>`. Writes go to the current
write index; rollover creates a new one; searches hit all backing indices.

## Templates
```json
PUT _component_template/app-logs-mappings
{ "template": { "mappings": { "properties": {
    "@timestamp": { "type": "date" },
    "service":    { "type": "keyword" },
    "level":      { "type": "keyword" },
    "message":    { "type": "text" } } } } }

PUT _component_template/app-logs-settings
{ "template": { "settings": {
    "index.lifecycle.name": "app-logs-policy",
    "number_of_shards": 1, "number_of_replicas": 1,
    "index.default_pipeline": "app-logs-pipeline" } } }

PUT _index_template/app-logs
{ "index_patterns": ["logs-app-*"],
  "data_stream": {},
  "composed_of": ["app-logs-mappings", "app-logs-settings"],
  "priority": 200 }
```
Indexing into a name matching the pattern auto-creates the stream:
```
POST logs-app-orders/_doc
{ "@timestamp": "2026-10-18T09:00:00Z", "service": "orders", "level": "ERROR", "message": "..." }
```
Every document **must** have `@timestamp` (or the configured timestamp field). Use
`op_type=create` semantics: bulk actions must be `create`, not `index`.

Naming: Elastic's convention `type-dataset-namespace` (e.g. `logs-nginx.access-prod`) matches
built-in templates with priority 100 for `logs-*-*`; give your template a higher priority or a
distinct pattern to avoid being overridden.

## Operations
```
GET _data_stream/logs-app-orders                 # backing indices, generation, ILM policy, health
POST logs-app-orders/_rollover                   # manual rollover (e.g. after a mapping change)
GET _data_stream/logs-app-orders/_stats
DELETE _data_stream/logs-app-orders              # deletes all backing indices
```
Mapping changes in templates apply at the **next rollover**; roll over to pick them up.

## Updates and deletes
Data streams are append-only: you cannot `index` an existing `_id` through the stream. Use
`_update_by_query` / `_delete_by_query` on the stream, or address a specific backing index with
`if_seq_no`/`if_primary_term` for single-document changes. If you need frequent updates, use a
regular index with an alias instead.

## Gotcha: logsdb mode
On 9.5.5 a data stream named `logs-*-*` reported `"index_mode": "logsdb"` in `GET _data_stream/<name>` even with a custom priority-200 template, so check `index_mode` if you rely on stored source or index sorting.

## Retention
ILM policy (hot -> warm -> delete), or data stream lifecycle (`"lifecycle": { "data_retention": "30d" }`
in the template) which is simpler for retention-only needs.

## Verify
`GET _data_stream/logs-app-orders` shows the template, `ilm_policy`, and status GREEN; new
documents land in the latest `.ds-` index; `GET _index_template/app-logs` resolves the components.
