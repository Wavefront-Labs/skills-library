---
id: computing-software.database-administration.elasticsearch.simulating-ingest-pipelines
name: simulating-ingest-pipelines
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, opensearch, ingest-pipeline, simulate-pipeline, pipeline-testing, verbose-simulate, ingest-simulate-api, pipeline-ci]
level: practitioner
status: verified
description: "Test Elasticsearch ingest pipelines before deploying them with the _simulate API (verbose per-processor output) and the _ingest/_simulate API with index templates."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/simulate-pipeline-api.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/simulate-ingest-api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Simulating ingest pipelines

**Goal:** catch parsing bugs on sample documents in seconds, without indexing
anything or touching production indices.

## Simulate a stored pipeline
```json
POST _ingest/pipeline/app-logs/_simulate?verbose=true
{
  "docs": [
    { "_index": "logs-app", "_source": { "message": "2026-10-16T14:03:12.511Z INFO [orders] 10.1.2.3 POST /api/orders 201 37ms" } },
    { "_source": { "message": "garbage line" } }
  ]
}
```
`verbose=true` shows the document after **each processor** with its status
(`success`, `error`, `skipped` for `if` conditions), which pinpoints the failing step.

## Simulate an unsaved pipeline definition
```json
POST _ingest/pipeline/_simulate
{
  "pipeline": { "processors": [ { "dissect": { "field": "message", "pattern": "%{ts} %{level} %{rest}" } } ] },
  "docs": [ { "_source": { "message": "2026-10-16T14:03:12Z WARN disk at 91%" } } ]
}
```
Iterate on the definition here, then `PUT _ingest/pipeline/<id>`.

## Simulate the whole indexing path
```json
POST _ingest/_simulate
{ "docs": [ { "_index": "logs-app-default", "_source": { "message": "..." } } ] }
```
Runs the default and final pipelines the target index would use (from its
template/settings) and can take `pipeline_substitutions` to test a new version
of a pipeline in context. It also reports mapping errors the
document would cause (give each doc an `_id`: without one 9.5 reports a spurious "_id should have been set" error). A string `"notanumber"` for a `long` field came back as `failed to parse field [n] of type [long]`, and `executed_pipelines` lists `["def", "fin"]`.

## Use in CI
Store pipelines and sample docs (good and bad lines) in the repo; a CI job
calls `_ingest/pipeline/_simulate` against a throwaway cluster and
asserts on expected fields and on `on_failure` behaviour for bad samples.

## Gotchas
- Simulation doesn't check whether the result fits the index mapping (except
  the newer `_ingest/_simulate`): a string in a long field still fails at index time.
- Processors relying on enrich policies or the `geoip` database need those to exist on the cluster.
- `_index`/`_id` in docs matter for processors that read metadata.

## Verify
Every sample's output contains the expected fields with correct types, and bad
samples follow the failure path (error field set, routed to a failure index).
