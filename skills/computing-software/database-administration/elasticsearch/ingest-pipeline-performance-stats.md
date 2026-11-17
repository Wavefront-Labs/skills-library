---
id: computing-software.database-administration.elasticsearch.ingest-pipeline-performance-stats
name: ingest-pipeline-performance-stats
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, ingest-stats, ingest-pipelines, node-stats, elasticsearch-ingest, performance]
level: practitioner
status: verified
description: "Measure Elasticsearch ingest pipeline cost per pipeline and processor from node stats, find slow processors, and decide on dedicated ingest nodes."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-stats.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ingest pipeline performance stats

**Goal:** know which pipeline and processor eats ingest CPU before indexing throughput collapses.

## Read the stats
```bash
GET _nodes/stats/ingest?filter_path=nodes.*.name,nodes.*.ingest.total,nodes.*.ingest.pipelines
```
Per pipeline: `count`, `time_in_millis`, `current`, `failed`; per processor (in order, with `type` and `tag`): the same counters. Stats are cumulative since node start; sample twice and diff.

Cost per document: `time_in_millis / count`. Rank processors by total time:
```bash
curl -s -u elastic --cacert ca.crt "https://es:9200/_nodes/stats/ingest" | python -c "import json,sys; d=json.load(sys.stdin); r=[(p['stats']['time_in_millis'],n,k) for v in d['nodes'].values() for n,pl in v['ingest']['pipelines'].items() for q in pl['processors'] for k,p in q.items()]; [print(*x) for x in sorted(r,reverse=True)[:10]]"
```
The processor key is the type, or `type:tag` when the processor has a `tag`.

## Measure, do not guess
On 9.5.5, 20,000 documents through a grok pipeline took 169 ms of processor time and through the equivalent dissect pipeline 31 ms (same example line as the grok/dissect skill), so the per-processor `time_in_millis` ranking above is how to find the expensive step.

## Where ingest runs
Ingest pipelines are processed by nodes with the `ingest` role (the cluster needs at least one); for heavy ingest load the docs recommend dedicated ingest nodes.

## Write thread pool symptoms
`GET _cat/thread_pool/write?v&h=node_name,active,queue,rejected` rising rejections together with high ingest `time_in_millis` points at pipeline CPU rather than disk; confirm with hot threads.

## Verify
After optimising a processor, the diffed `time_in_millis/count` for it drops and bulk throughput (docs/s) rises at the same CPU.
