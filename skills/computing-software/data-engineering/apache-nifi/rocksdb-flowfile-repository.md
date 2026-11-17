---
id: computing-software.data-engineering.apache-nifi.rocksdb-flowfile-repository
name: rocksdb-flowfile-repository
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, rocksdb, flowfile-repository, deprecated, tuning]
level: sme
status: docs-checked
description: "Deprecated RocksDB FlowFile repository in NiFi: NiFi-side stall, stop, recovery and sync keys plus RocksDB-side buffer and compaction keys, with defaults."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RocksDB FlowFile repository (deprecated)

The admin guide says RocksDBFlowFileRepository is deprecated in favor of WriteAheadFlowFileRepository and will be removed in future major versions; in NiFi 1.x it needs nifi-rocksdb-nar from the Apache Nexus Repository placed in the lib directory.

NiFi-side keys under `nifi.flowfile.repository.rocksdb.`:
- `sync.period` 10 milliseconds; `sync.warning.period` 30 seconds; `claim.cleanup.period` 30 seconds
- `deserialization.threads` 16; `deserialization.buffer.size` 1000
- `accept.data.loss` false; `remove.orphaned.flowfiles.on.startup` false
- `enable.stall.stop` false; `stall.period` 100 ms; `stall.flowfile.count` 800000; `stall.heap.usage.percent` 95%
- `stop.flowfile.count` 1100000; `stop.heap.usage.percent` 99.9%
- `enable.recovery.mode` false (limits FlowFiles loaded into the graph to recover from out-of-memory errors on startup; enable only to recover, do not modify the graph while on); `recovery.mode.flowfile.count` 5000

RocksDB-side keys:
- `parallel.threads` 8; `max.write.buffer.number` 4; `write.buffer.size` 256 MB
- `level.0.slowdown.writes.trigger` 20; `level.0.stop.writes.trigger` 40
- `delayed.write.bytes.per.second` 16 MB
- `max.background.flushes` 1; `max.background.compactions` 1
- `min.write.buffer.number.to.merge` 1; `stat.dump.period` 600 sec

Verify: with stall enabled, a deliberately full queue slows ingestion rather than exhausting heap.

## Checked

Confirmed in the NiFi Administration Guide, RocksDB FlowFile Repository properties: every NiFi-side and RocksDB-side key and default listed above (stall period is given as 100 milliseconds), the deprecation notice and the recovery mode description. Nothing was removed.

Method: docs-only read of cited pages, 2026-11-08
