---
id: computing-software.data-engineering.apache-kafka.kafka-streams-state-stores
name: kafka-streams-state-stores
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-streams, kafka-streams-state-store, changelog-topic, rocksdb, standby-replicas, state-restoration, interactive-queries, statefulset, warmup-replicas]
level: sme
status: docs-checked
description: "Operate Kafka Streams state stores: RocksDB + changelog topics, restoration time, standby replicas, persistent volumes, RocksDB memory bounding, and interactive queries."
sources:
  - https://kafka.apache.org/39/streams/developer-guide/processor-api/
  - https://kafka.apache.org/39/streams/developer-guide/memory-mgmt/
  - https://kafka.apache.org/39/streams/developer-guide/interactive-queries/
  - https://kafka.apache.org/39/streams/developer-guide/config-streams/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka Streams state stores

**Goal:** stateful Streams apps restart fast, fail over without long outages, and do not exhaust memory.

## Anatomy
- Each stateful operation (aggregate, join, `Materialized.as`) has a local store, default **RocksDB** on disk under `state.dir`.
- Fault-tolerant stores are backed by a compacted **changelog topic**: the durable copy (you can disable it per store with `withLoggingDisabled()`, which removes fault tolerance).
- On a new instance or lost disk, the task **restores** the store from the changelog before processing.

## Fast recovery
```properties
num.standby.replicas=1                 # keep a hot copy of each store on another instance
acceptable.recovery.lag=10000          # default: max offset lag for an instance to count as caught up
max.warmup.replicas=2                  # default: extra standbys (warmups) assigned at once
state.dir=/data/kafka-streams          # persistent volume
```
- Keep `state.dir` on a persistent volume so a restarted instance reuses its local state.

## Bound RocksDB memory
RocksDB memory (block cache, memtables, index/filter blocks) is not bounded by default and is used per store instance. Bound it with a shared cache and write buffer manager via `rocksdb.config.setter` (the memory management page has the reference example):
```java
public class BoundedMemory implements RocksDBConfigSetter {
  private static final long TOTAL = 512L << 20, MEMTABLES = 128L << 20;
  private static final Cache CACHE = new LRUCache(TOTAL, -1, false, 0.1);
  private static final WriteBufferManager WBM = new WriteBufferManager(MEMTABLES, CACHE);
  public void setConfig(String store, Options o, Map<String, Object> c) {
    BlockBasedTableConfig t = (BlockBasedTableConfig) o.tableFormatConfig();
    t.setBlockCache(CACHE); t.setCacheIndexAndFilterBlocks(true);
    o.setWriteBufferManager(WBM); o.setTableFormatConfig(t);
  }
  public void close(String store, Options o) {}
}
```
Also: `statestore.cache.max.bytes` (record caches across all threads; default 10485760 bytes).

## Store hygiene
- Window store changelogs use compaction and deletion; the default retention is `Windows#maintainMs()` + 1 day, which you can override.
- Plan broker disk for the changelog topics.
- In-memory stores (`Stores.inMemoryKeyValueStore`) are also backed by a changelog.

## Interactive queries
Query a store through `KafkaStreams#store` with `QueryableStoreTypes.keyValueStore()`. Each instance holds only its partitions: set `application.server` (host:port, different for each instance) and use the metadata methods (the 3.9 page shows `metadataForKey(storeName, key, keySerializer)`) to find the owning host and route the request there. Check the page for newer replacements of these methods.

## Checked
2026-10-28. Confirmed on the Kafka 3.9 Streams pages: RocksDB/changelog behaviour, compaction and deletion for window changelogs and the `maintainMs() + 1 day` default, `withLoggingDisabled()`, `num.standby.replicas`, `acceptable.recovery.lag` (10000), `max.warmup.replicas` (2), `statestore.cache.max.bytes` (10485760), `rocksdb.config.setter`, the shared `LRUCache`/`WriteBufferManager` example, `application.server`, `metadataForKey`. Removed: restore metric names, listener name, OOM sizing example, `StoreQueryParameters` call (not on the 3.9 page), tombstone and standby-verify claims.
Method: documentation only; no commands were run.

## Verify
- [ ] Restart one instance: processing resumes in seconds (local state reused), not after full restore.
- [ ] Container memory under load stays below limit with the bounded RocksDB config.
