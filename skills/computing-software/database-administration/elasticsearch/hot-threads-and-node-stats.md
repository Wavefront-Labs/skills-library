---
id: computing-software.database-administration.elasticsearch.hot-threads-and-node-stats
name: hot-threads-and-node-stats
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, hot-threads, node-stats, thread-pool-rejections, cat-thread-pool, jvm-gc, cpu-troubleshooting, tasks-api]
level: practitioner
status: verified
description: "Troubleshoot Elasticsearch CPU and latency with nodes hot_threads, nodes stats, _cat/thread_pool rejections, JVM GC data and the tasks API."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-hot-threads.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-stats.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-thread-pool.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hot threads and node stats

**Goal:** when a node pegs CPU or requests get rejected, find what it is doing within minutes.

## Hot threads
```bash
GET _nodes/hot_threads?threads=5&interval=500ms&type=cpu     # all nodes
GET _nodes/es-data-07/hot_threads?type=wait
```
Text output: per node, the busiest threads with CPU percentages and stack traces; read the thread name and the top frames to see whether search, write, merge or management work dominates.

## Thread pools and rejections
```bash
GET _cat/thread_pool/search,write,get?v&h=node_name,name,active,queue,rejected,completed
```
Rising `rejected` on `write` means bulk queues overflow (HTTP 429 `es_rejected_execution_exception`): clients must back off/retry; fix hot shards or add capacity, do not just raise queue sizes.

## Node stats
```bash
GET _nodes/stats/jvm,os,process,fs,indices,breaker,thread_pool
GET _cat/nodes?v&h=name,role,heap.percent,ram.percent,cpu,load_1m,disk.used_percent
```
Watch:
- `jvm.mem.heap_used_percent` staying high between GCs, `jvm.gc.collectors.old.collection_time_in_millis` rising: heap pressure.
- `indices.search.query_time_in_millis / query_total` per node: one slow node = hot shard or bad hardware.
- `fs.io_stats` and `os.cpu.load_average` (Linux only: both were absent in node stats on Windows).
- `indices.segments.count` and merges.

## Running tasks
```bash
GET _tasks?detailed=true&actions=*search*
GET _cat/tasks?v&detailed
POST _tasks/<task_id>/_cancel
```
`X-Opaque-Id` on the task identifies the client.

## Hot shard check
```bash
GET _cat/shards/orders?v&h=index,shard,prirep,node,docs,store&s=store:desc
```
Uneven primaries on one node or a skewed routing key concentrates load: rebalance with `index.routing.allocation.total_shards_per_node` (the dynamic index setting was accepted) or more shards.

## Verify
After the fix, hot_threads no longer shows the offending stack, `rejected` stops growing and node CPU evens out.
