---
id: computing-software.data-engineering.druid.druid-basic-cluster-tuning
name: druid-basic-cluster-tuning
category: computing-software
field: data-engineering
product: druid
tags: [tuning, heap-sizing, historical, lookups, garbage-collector, cache]
level: advanced
status: docs-checked
description: "Apply Druid's documented rules of thumb for heap, direct memory, thread pools and connection pools per service, plus JVM and OS settings."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/basic-cluster-tuning.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The guide gives starting points, not absolute rules, and is not an exhaustive list of tuning properties. Test changes in staging.

## Historical

- Heap: biggest consumers are partial unmerged query results and lookup maps. Start at 0.5 GiB times CPU cores, plus 2x the total size of loaded lookups (old and new maps coexist during the atomic swap), plus `druid.cache.sizeInBytes` if the on-heap cache is enabled. For heaps above about 24 GiB use a large-heap collector such as Shenandoah or ZGC.
- Threads and buffers: `druid.processing.numThreads` = cores minus 1; `druid.processing.buffer.sizeBytes` 500 MiB; `druid.processing.numMergeBuffers` about 1 per 4 processing threads.
- Direct memory = (`numThreads` + `numMergeBuffers` + 1) x `buffer.sizeBytes`. The +1 is a fuzzy allowance for segment decompression buffers.
- HTTP threads: `druid.server.http.numThreads` slightly above the sum of `druid.broker.http.numConnections` across all Brokers. A starting target is 50 query plus 10 non-query connections per Historical (so 60).
- Segment cache: do not assign more segment data than free system memory; size follows `druid.segmentCache.locations` (override with `druid.server.maxSize` only in rare cases). Aim for a good ratio of free system memory to total segment cache size. Fewer big servers beat many small ones if fault tolerance allows. Use SSDs.

## Broker

- Heap holds partial results, the segment timeline and cached segment metadata, and scales with segment count and data size. 4-8 GiB for small or medium clusters (about 15 servers or fewer); very large clusters (about 100 nodes) may need 30-60 GiB.
- Direct memory depends on merge buffers only: (`numMergeBuffers` + 1) x `buffer.sizeBytes`; set `numMergeBuffers` equal to or a bit above Historicals, buffer size 500 MiB. Brokers merge results on heap so need no processing threads.
- Connections: the sum of `druid.broker.http.numConnections` across Brokers should be slightly below `druid.server.http.numThreads` on Historicals and Tasks; Broker `druid.server.http.numThreads` slightly above its own `numConnections`.
- Backpressure: `druid.broker.http.maxQueuedBytes`, split across the servers a query fans out to; roughly 2 MiB x number of Historicals. Too small stalls channels; too large adds Broker memory pressure.
- Roughly 1 Broker per 15 Historicals; start with 2 for HA.

## Middle Manager and Tasks

- Middle Manager heap about 128 MiB. Capacity is `druid.worker.capacity`. Use SSDs.
- Task heap 1 GiB plus 2x lookup maps. Per-task via `druid.indexer.fork.property.`: `druid.processing.numThreads` 1 or 2, `numMergeBuffers` 2, `buffer.sizeBytes` 100 MiB. Same direct memory formula (the +1 also covers dictionary merging buffers). Same 50 query plus 10 non-query HTTP guideline.
- Total = Middle Manager heap + `druid.worker.capacity` x single-task memory.
- Kafka/Kinesis: task count depends on partitions and `taskCount`/replicas; leave spare slots for compaction. Parallel native batch also benefits from extra slots.

## Coordinator, Overlord, Router

- Coordinator: heap scales with servers, segments and tasks; same as the Broker heap or slightly smaller. Dynamic config `percentOfSegmentsToConsiderPerMove` defaults to 100; if full coordination cycles take too long and `maxSegmentsToMove` (default 5) is above 0, try about 66. Little gain on small clusters.
- Overlord: heap scales with running tasks; about 25-50% of the Coordinator heap.
- Router: about 256 MiB to start.

## Processing buffers and connections

- `druid.processing.buffer.sizeBytes`: one per processing thread, 500 MiB to 1 GiB typical; TopN and GroupBy use them.
- GroupBy merge buffers (same size as processing buffers): 1 per non-nested query, 2 per nested query; the count caps concurrent GroupBys. Tune with metrics from `org.apache.druid.server.metrics.GroupByStatsMonitor`: `mergeBuffer/maxBytesUsed`, `groupBy/maxSpilledBytes`, `groupBy/spilledQueries` (buffer too small), `mergeBuffer/pendingRequests`, `mergeBuffer/maxAcquisitionTimeNs` (too few buffers), `groupBy/maxMergeDictionarySize` versus `druid.query.groupBy.maxMergingDictionarySize`.
- `druid.broker.http.numConnections` is effectively the cap on concurrent queries per Broker. Example: 3 Brokers at 10 connections give 30 query connections per Historical, so set `numThreads` to 40 (30 plus 10 non-query). Pools too small underuse the cluster; too large risks out-of-memory. Sizing matters most with QoS and priorities; many sub-15ms queries justify a larger pool.
- Per-segment direct memory: a 64 KiB decompression buffer per column read per segment; during ingestion merges, a buffer per string column per segment of cardinality x 4 bytes (independent of `numMergeBuffers`).

## JVM and OS

- Use G1GC (`-XX:+UseG1GC`) and `-XX:+ExitOnOutOfMemoryError` (JDK 8u92 or later; older JVMs use `-XX:OnOutOfMemoryError`). The page lists general flags: `-Duser.timezone=UTC`, `-Dfile.encoding=UTF-8`, a `java.io.tmpdir` that is not volatile tmpfs and not NFS, GC logging with rotation, `-XX:+HeapDumpOnOutOfMemoryError` and `-XX:MaxDirectMemorySize`. These are samples only; make sure total off-heap allocation fits the machine.
- Large-heap GC hints: mount /tmp on tmpfs, write GC and Druid logs to a different disk than data on I/O-heavy processes, disable Transparent Huge Pages, try `-XX:-UseBiasedLocking`.
- Use UTC everywhere; query other time zones via period granularities.
- System: SSDs for Historical, Middle Manager and Indexer unless fully in memory; JBOD may beat software RAID for Historicals; no swap; raise the open-files `ulimit` well above the segment file count and `vm.max_map_count` for memory-mapped segments.

## Checked

2026-11-08. Read the cited basic-cluster-tuning page in full. Replaced the Historical-only draft with the per-service sizing rules, formulas, connection-pool arithmetic and JVM/OS settings; omitted the sample file paths from the JVM flags.

Method: documentation only; no commands were run.
