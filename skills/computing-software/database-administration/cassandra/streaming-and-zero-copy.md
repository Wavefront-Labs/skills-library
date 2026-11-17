---
id: computing-software.database-administration.cassandra.streaming-and-zero-copy
name: streaming-and-zero-copy
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, stream-throughput, zero-copy-streaming, netstats-streams, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Bulk data movement"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/architecture/streaming.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming and zero-copy streaming

Goal: move SSTables between nodes fast.
- Zero-copy streaming is controlled by `stream_entire_sstables` (default true) and sends whole SSTables, every component, when all partitions in the SSTable need to be transmitted; this is common with LeveledCompactionStrategy.
- It is automatically disabled when internode encryption is enabled.
- Throttle with `stream_throughput_outbound` (default 24MiB/s) and `inter_dc_stream_throughput_outbound`.
- Watch progress with `nodetool netstats`.
Verify: streaming completes at roughly the configured cap.

## Checked

2026-11-02. Checked against the Streaming page (stream_entire_sstables default, eligibility, disabled with internode encryption, stream_throughput_outbound default, inter_dc setting) and topo_changes (netstats). Removed: the list of operations that stream and '4.0' version claim (not on the page).

Method: documentation only; no commands were run.
