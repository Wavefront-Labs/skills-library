---
id: computing-software.database-administration.cassandra.concurrency-and-throughput
name: concurrency-and-throughput
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, concurrent-reads, concurrent-writes, compaction-throughput, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Thread pools and throttles"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Concurrency and throughput settings

Goal: tune throughput.
- `concurrent_reads` (about 16 x data disks), `concurrent_writes` (about 8 x cores), `concurrent_compactors`.
- `compaction_throughput` (`64MiB/s` in the shipped cassandra.yaml) adjusts live with `nodetool setcompactionthroughput`.
- Also `stream_throughput_outbound`, `native_transport_max_threads`. Change one thing at a time.
Verify: p99 improves without raising pending compactions.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: concurrent_reads (16 x drives), concurrent_writes (8 x cores), concurrent_compactors, compaction_throughput default 64MiB/s, stream_throughput_outbound, native_transport_max_threads (cassandra.yaml); setcompactionthroughput (compaction overview).
Removed: the `64 MB/s` unit (the file says MiB/s).
Method: documentation only; no commands were run.
