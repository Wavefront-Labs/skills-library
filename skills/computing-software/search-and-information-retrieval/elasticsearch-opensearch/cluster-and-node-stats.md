---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.cluster-and-node-stats
name: cluster-and-node-stats
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, cluster-and-node-stats, es-monitoring]
level: practitioner
status: docs-checked
description: "Collect key health metrics from _cluster/stats, _nodes/stats and _cat APIs and alert on them."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-stats.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-stats.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-pending.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster and node stats

**Goal:** a metric set that predicts trouble.
- `GET _nodes/stats/jvm,os,fs,indices,thread_pool` for heap, OS, file system, index (search, indexing and other per-index metrics) and thread pool statistics; `thread_pool` reports current size, queue and rejected tasks. `GET _cluster/stats` gives cluster-wide statistics.
- Alert candidates: cluster status, heap percent sustained, disk watermark proximity, pending cluster-state updates from `GET _cluster/pending_tasks`, rejected thread pool tasks (`rejected` counter).
- Keep monitoring data in a separate cluster where possible.
- Failure mode: monitoring the cluster from inside itself disappears exactly when it is red.

## Verify
- [ ] Stopping a data node in staging triggers the node-count and status alerts.

## Notes
- Try every request on a test index first; syntax and defaults differ between Elasticsearch and OpenSearch versions, so check the linked reference for yours.
- Cited pages are Elasticsearch; OpenSearch behaviour was not checked here.

## Checked
2026-11-08. Read the Elasticsearch nodes stats, cluster stats and pending tasks API pages: metric names (`jvm`, `os`, `fs`, `indices`, `thread_pool`), thread pool rejected counter, `GET /_cluster/pending_tasks`. Removed the Prometheus exporter and Metricbeat/Elastic Agent export claim (not on these pages); the separate monitoring cluster is advice.
Method: documentation only; no commands were run.
