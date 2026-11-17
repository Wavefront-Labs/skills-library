---
id: computing-software.database-administration.elasticsearch.default-pipeline-and-final-pipeline
name: default-pipeline-and-final-pipeline
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, final-pipeline, default-pipeline, ingest-pipelines, index-settings, elasticsearch-ingest]
level: practitioner
status: verified
description: "Attach Elasticsearch ingest pipelines to indices with index.default_pipeline and index.final_pipeline, override per request, and enforce processing clients cannot skip."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html#index-default-pipeline
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html#set-default-pipeline
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# default_pipeline and final_pipeline

## Behaviour
| Setting | Runs when | Can the client skip it? |
|---|---|---|
| `index.default_pipeline` | No `?pipeline=` given on the request | Yes: `?pipeline=_none` or another pipeline replaces it |
| `index.final_pipeline` | Always, after the default or request pipeline | No |

Order: request pipeline (or default) → final pipeline.

## Set via index template (for data streams and rollovers)
```json
PUT _index_template/logs-app
{ "index_patterns": ["logs-app-*"], "data_stream": {},
  "template": { "settings": {
    "index.default_pipeline": "logs-app-parse",
    "index.final_pipeline": "logs-enforce" } } }
```
Changing an existing index: `PUT logs-app-000001/_settings { "index.final_pipeline": "logs-enforce" }`.

## Good uses for final_pipeline
- Add `event.ingested` timestamp, cluster/env labels.
- Remove forbidden fields (PII scrubbing) regardless of which client or Beat sends data.
- Validate and route: fail documents missing required fields into an error index.

## Gotchas
- Setting `_index` in a pipeline redirects the document (a pipeline-level `on_failure` that set `_index` to `failed-{{ _index }}` put the document in that index); test rerouting flows end to end, including whether the target index's own pipelines run.
- Missing pipeline name in settings makes every write fail (`pipeline with id [x] does not exist`). Create the pipeline first.
- Elastic Agent integrations set their own default pipelines; the Fleet docs describe adding custom logic with a `<type>-<dataset>@custom` pipeline (their example is `metrics-system.cpu@custom`) rather than replacing the integration's.

## Verify
Index a test document without `?pipeline` and with `?pipeline=_none`; on 9.5.5 the final pipeline's `event.ingested` was present in both, while the default pipeline's field was missing from the `_none` one.
