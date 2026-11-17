---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-dependencies-graph
name: jaeger-dependencies-graph
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, service-dependencies, spark-dependencies, deep-dependency-graph, system-architecture-graph]
level: practitioner
status: docs-checked
description: "Populate the Dependencies page on real storage with the spark-dependencies job, and know the two topology graph types."
sources:
  - https://www.jaegertracing.io/docs/2.22/faq/
  - https://www.jaegertracing.io/docs/2.22/architecture/apis/
  - https://www.jaegertracing.io/docs/2.22/deployment/frontend-ui/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: fix an empty Dependencies page.

With in-memory storage the graph is calculated on demand from stored traces. With Cassandra, Elasticsearch or OpenSearch, scanning all data is too expensive, so the Jaeger project provides big-data jobs:
- spark-dependencies (older Spark job that can be run periodically)
- jaeger-analytics (new, experimental): streaming Flink jobs that run continuously and build the graph in smaller intervals.

UI settings: `dependencies.menuEnabled` (default true) and `dependencies.dagMaxNumServices` (default 200).

API: GET `/api/dependencies?endTs=<ms>&lookback=<ms>` returns (caller, callee, count) tuples; it is an internal API.

## Checked

2026-11-03. Confirmed against the FAQ page (empty Dependencies page, in-memory versus real storage, spark-dependencies and jaeger-analytics), the APIs page (/api/dependencies, internal) and the Frontend/UI page (dependencies.menuEnabled and dagMaxNumServices defaults). Removed: the description of the System Architecture and Deep Dependency Graph types and the claims about how spark-dependencies writes data and that production needs it, none of which the fetched pages state.
Method: documentation only; no commands were run.
