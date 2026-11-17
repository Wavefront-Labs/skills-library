---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-memory-storage
name: jaeger-memory-storage
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, memory-storage, max-traces, transient-storage]
level: intro
status: docs-checked
description: "Use in-memory trace storage for quick starts and cap it with max_traces; it is not for production."
sources:
  - https://www.jaegertracing.io/docs/2.22/storage/memory/
  - https://www.jaegertracing.io/docs/2.22/faq/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure the memory backend.

The in-memory storage is not intended for production workloads. It is a simple way to get started and data is lost once the process exits.

By default there is no limit on the number of traces stored. Set a cap with `max_traces`:
```
jaeger_storage:
  backends:
    some_store:
      memory:
        max_traces: 100000
```
With in-memory storage the Dependencies page graph is calculated on demand from all the traces stored in memory. With distributed storage like Cassandra, Elasticsearch or OpenSearch that scan is too expensive, so the project provides separate jobs (spark-dependencies, the experimental jaeger-analytics Flink jobs) to extract the service graph.

Summary: use memory only for demos and tests, and set max_traces to bound memory use.

## Checked

2026-11-08: read the whole Memory page and the FAQ (raw markdown from the jaegertracing/documentation repo, v2/2.22). Confirmed the production warning, max_traces config, and the dependencies-graph FAQ answer. Removed unsupported claims: all-in-one default storage, adaptive sampling store use, the collector/query sharing failure mode, and the Badger recommendation.

Method: documentation only; no commands were run.
