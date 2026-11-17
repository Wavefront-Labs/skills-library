---
id: computing-software.database-administration.elasticsearch.high-jvm-memory-pressure
name: high-jvm-memory-pressure
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-operations, jvm-memory-pressure, heap-size, garbage-collection, circuit-breaker, fielddata]
level: advanced
status: docs-checked
description: "Diagnose high JVM memory pressure on Elasticsearch nodes: heap usage after GC, GC logs, big consumers (fielddata, aggregations, shard count) and fixes before OOM."
sources:
  - https://github.com/elastic/docs-content/blob/main/troubleshoot/elasticsearch/high-jvm-memory-pressure.md
  - https://github.com/elastic/docs-content/blob/main/deploy-manage/deploy/self-managed/important-settings-configuration.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/jvm-settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# High JVM memory pressure

## Measure
```
GET _nodes/stats/jvm?filter_path=nodes.*.name,nodes.*.jvm.mem.heap_used_percent,nodes.*.jvm.mem.pools.old,nodes.*.jvm.gc
GET _cat/nodes?v&h=name,heap.percent,heap.max,ram.percent,cpu,load_1m,node.role
```
High JVM memory usage can degrade performance and trigger circuit breaker errors. Elastic Cloud's per-node memory pressure indicator turns red at 75%. As usage rises, garbage collection becomes more frequent and slower; track GC events in `elasticsearch.log` and the GC log (`gc.log`). Long or back-to-back old GCs are a warning sign.

## Common causes
| Cause | Check | Fix |
|---|---|---|
| too many shards per node | `GET _cat/shards?v` count per node; `_cluster/stats` | fewer, larger shards (a small set of large shards uses fewer resources than many small ones), shrink/merge, delete old indices, ILM |
| fielddata on text fields | `GET _cat/fielddata?v` | disable `fielddata: true`; aggregate on keyword fields |
| expensive aggregations (huge `terms` size, deep nested aggs) | slow logs, tasks | composite aggregation paging, smaller `size`, `shard_size` |
| large bulk requests / big documents | indexing pressure stats | spread out bulk and multi-search requests (smaller batches) |
| deep pagination with `from`/`size` | search slow log | `search_after` + PIT |
| many mapped fields (mapping explosion) | `_mapping` field count | flattened type, `dynamic: false`, field limits |
| heap undersized for workload | `heap.max` vs RAM | heap no more than 50% of RAM and under the compressed-oops threshold |

## Heap sizing
By default ES sizes the heap automatically from node roles and total memory. To override, add a file under `jvm.options.d/` (for example `config/jvm.options.d/heap.options` for archive installs; `/etc/elasticsearch/jvm.options.d/` for DEB/RPM). Do not edit the root `jvm.options`:
```
-Xms16g
-Xmx16g
```
`Xms` and `Xmx` must be equal and no more than 50% of the node's memory; Elasticsearch also needs off-heap memory and the OS filesystem cache. The compressed-oops threshold varies (26 GB is safe on most systems, up to about 30 GB on some); verify with `jvm.using_compressed_ordinary_object_pointers` in `GET _nodes` or the startup log line.

## Immediate relief
- Clear fielddata cache: `POST _cache/clear?fielddata=true`.
- Cancel runaway searches: `GET _tasks?actions=*search*&detailed`, then
  `POST _tasks/<task_id>/_cancel`.
- Rolling restart only resets the symptom; find the cause.

## Verify
Heap usage stays well below the 75% indicator under normal load, GC pauses are short, and
`_nodes/stats/breaker` shows no recent `tripped` increments.

## Checked

Checked 2026-10-25 against elastic/docs-content and elastic/elasticsearch `main` docs (Stack 9.x). Confirmed: 75% Cloud indicator, automatic heap sizing, `jvm.options.d` locations and the do-not-edit-`jvm.options` rule, `Xms`=`Xmx` and the 50% rule, compressed-oops threshold guidance, fielddata cache clearing API, bulk and shard-count advice. Removed the unconfirmed 85% threshold, 10-50 GB shard size, 5-15 MB bulk size, `7.11+` and breaker-limit tuning claims. The `_nodes/stats/jvm` filter_path in Measure and the task cancel calls were not re-read.

Method: documentation only; no commands were run.
