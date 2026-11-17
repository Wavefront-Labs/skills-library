---
id: computing-software.database-administration.cassandra.heap-and-gc-tuning
name: heap-and-gc-tuning
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, heap-size, max-heap, zgc, jvm-options, cassandra-gc, g1gc, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Sizing the heap"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heap sizing and garbage collector

Goal: choose heap and GC.
- Hardware guide: heap no less than 2GB and no more than 50% of system RAM; leave the rest for page cache. G1 is enabled in `jvm11-server.options` and `jvm17-server.options`.
- Set in `jvm-server.options` and the per-JDK file, not by editing scripts.
- `jvm21-server.options` ships Generational ZGC settings (`-XX:+UseZGC`).
- Read `gc.log` and correlate pauses with dropped messages.
Verify: pauses seen in `gc.log` no longer line up with dropped messages.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: heap 2GB-50% RAM guidance (hardware page), UseG1GC in jvm11/jvm17 options, UseZGC in jvm21 options, jvm-server.options file.
Removed: the 8-16 GB typical heap, the Shenandoah/5.0 claim and the 500 ms target.
Method: documentation only; no commands were run.
