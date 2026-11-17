---
id: computing-software.data-engineering.apache-flink.rocksdb-tuning
name: rocksdb-tuning
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, rocksdb-tuning, rocksdb, managed-memory, state-backend, compaction]
level: advanced
status: docs-checked
description: "Tune Flink's RocksDB state backend: managed memory sizing, write buffer and block cache ratios, predefined options, local SSDs, compaction and native metrics."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RocksDB memory and performance tuning

## Memory: let Flink manage it
```yaml
state.backend.type: rocksdb
state.backend.rocksdb.memory.managed: true          # default: all RocksDB instances in a slot share managed memory
taskmanager.memory.managed.fraction: 0.4            # default 0.4 of total Flink memory; raise for state-heavy jobs
state.backend.rocksdb.memory.write-buffer-ratio: 0.5    # share for memtables
state.backend.rocksdb.memory.high-prio-pool-ratio: 0.1  # index/filter blocks kept hot
```
- Managed memory is split per slot; every stateful operator in the slot (each with a RocksDB instance and one column family per state) shares it.
- Read-heavy (large lookups): lower `write-buffer-ratio` to give the block cache more. Write-heavy: raise it.
- `state.backend.rocksdb.memory.fixed-per-slot: 1gb` overrides the fraction with a fixed amount.
- Container OOM kills with RocksDB usually mean memory outside the managed budget (many states with unmanaged options, index/filter blocks not in cache, glibc fragmentation). Keep `memory.managed=true`.

## Disk
- `state.backend.rocksdb.localdir`: fast local NVMe/SSD, not network volumes. RocksDB is I/O bound on cold reads and compaction.

## Predefined options and knobs
```yaml
state.backend.rocksdb.predefined-options: SPINNING_DISK_OPTIMIZED_HIGH_MEM   # or FLASH_SSD_OPTIMIZED; DEFAULT otherwise
state.backend.rocksdb.thread.num: 4                   # background flush/compaction threads (default 2)
state.backend.rocksdb.compaction.level.use-dynamic-size: true
state.backend.rocksdb.block.blocksize: 16kb           # larger for scans, smaller for point lookups
state.backend.rocksdb.use-bloom-filter: true          # default false
```
Programmatic: implement `RocksDBOptionsFactory` for anything else.

## Access-pattern fixes (bigger wins than knobs)
- `MapState` iterate-all is a range scan; `ValueState<List>` rewrites the whole list per update. Use `ListState` for append-heavy, `MapState` for per-entry updates.
- Every access serialises/deserialises: use efficient serializers (POJO/Avro), not Kryo; avoid huge values.
- Incremental checkpoints (`execution.checkpointing.incremental: true`) are essential for large RocksDB state.

## Native metrics
```yaml
state.backend.rocksdb.metrics.estimate-num-keys: true
state.backend.rocksdb.metrics.block-cache-usage: true
state.backend.rocksdb.metrics.num-running-compactions: true
state.backend.rocksdb.metrics.estimate-pending-compaction-bytes: true
state.backend.rocksdb.metrics.background-errors: true
```
Rising pending compaction bytes = write stalls ahead; add threads/faster disks. Each metric has overhead; enable selectively.

## Verify
- [ ] Busy time / backpressure drops on the stateful operator after tuning; checkpoint duration stable.
- [ ] Container RSS flat under steady load.

## Checked
2026-10-31. Confirmed against the Flink stable configuration page: every `state.backend.rocksdb.*` key above, `taskmanager.memory.managed.fraction` (default 0.4), `state.backend.rocksdb.memory.managed` (default true), write-buffer-ratio 0.5, high-prio-pool-ratio 0.1, thread.num default 2, predefined option names, `execution.checkpointing.incremental`. Removed: jemalloc remark, version gate on the bloom filter, the Kubernetes volume tip and the TTL compaction-filter line (not on these pages).
Method: documentation only; no commands were run.
