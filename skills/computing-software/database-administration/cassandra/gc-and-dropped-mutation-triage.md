---
id: computing-software.database-administration.cassandra.gc-and-dropped-mutation-triage
name: gc-and-dropped-mutation-triage
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, dropped-mutations, long-gc-pause, overloaded-node, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Overload triage"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/metrics.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/operating/hints.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/nodetool.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GC pauses and dropped messages

Goal: stabilise an overloaded node.
- Dropped messages are tracked per message type (DroppedMessage metrics); dropped writes are stored and retried by hinted handoff. The write timeout is `write_request_timeout` in cassandra.yaml.
- Find the cause before raising timeouts: `nodetool gcstats` (GC), `nodetool compactionstats` (compactions), `nodetool tpstats` (thread pools).
- Throttle client concurrency.
Verify: the DroppedMessage metrics stop increasing after the fix.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: DroppedMessage metrics, `write_request_timeout`, nodetool `gcstats`, `compactionstats`, `tpstats`. Removed: the `iostat -x` step (an OS tool outside the docs) and the claim that dropped mutations always mean coordinator timeouts.

Method: documentation only; no commands were run.
