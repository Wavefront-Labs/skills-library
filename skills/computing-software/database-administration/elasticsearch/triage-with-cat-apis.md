---
id: computing-software.database-administration.elasticsearch.triage-with-cat-apis
name: triage-with-cat-apis
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, cat-api, cluster-health, elasticsearch-operations, troubleshooting]
level: practitioner
status: verified
description: "Triage an Elasticsearch cluster fast with the _cat APIs: health, nodes, indices, shards, allocation, thread_pool, recovery, with useful columns, sorting and filtering."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cat.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-shards.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triage with the _cat APIs

**Goal:** a five-minute health sweep from a terminal. `_cat` is for humans; use JSON APIs for automation.

## Common flags
`?v` headers, `?help` lists columns, `h=` choose columns, `s=` sort (`s=store.size:desc`), `bytes=gb`, `format=json`.

## The sweep
```bash
GET _cat/health?v                                   # status, nodes, shards, unassign, pending_tasks
GET _cat/nodes?v&h=name,role,master,heap.percent,ram.percent,cpu,load_1m,disk.used_percent&s=heap.percent:desc
GET _cat/allocation?v&s=disk.percent:desc           # disk per node vs watermarks
GET _cat/indices?v&health=yellow                    # or red
GET _cat/indices?v&s=store.size:desc&h=index,health,pri,rep,docs.count,store.size | head -20
GET _cat/shards?v&h=index,shard,prirep,state,unassigned.reason,node&s=state | grep -v STARTED
GET _cat/recovery?v&active_only=true&h=index,shard,stage,source_node,target_node,bytes_percent,time
GET _cat/thread_pool/write,search?v&h=node_name,name,active,queue,rejected
GET _cat/pending_tasks?v
GET _cat/master?v
```

## Reading results
- Yellow: replicas unassigned (single node, awareness, disk). Red: a primary is unassigned; data for those shards is unavailable.
- For any unassigned shard: `GET _cluster/allocation/explain` with index/shard/primary gives the exact reason.
- `rejected` on write/search pools: overload; back-pressure clients or add capacity.
- Heap consistently high on a node (`heap.percent` against `heap.max`): see the high JVM memory pressure procedures.
- `_cat/segments` and `_cat/fielddata?v` help with memory deep dives.

## Gotchas
- `_cat/indices` on clusters with tens of thousands of indices is heavy; filter by pattern (`_cat/indices/logs-*`).
- `store.size` is primaries plus replicas; `pri.store.size` is primaries only (both columns exist).
- Do not parse `_cat` text in scripts; columns change between versions.

## Verify
Keep the sweep as a saved Dev Tools snippet or script and run it during every incident; compare against a baseline captured when healthy.
