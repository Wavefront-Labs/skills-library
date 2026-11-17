---
id: computing-software.database-administration.cassandra.tunable-consistency-levels
name: tunable-consistency-levels
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, local-quorum, each-quorum, read-write-quorum, consistency-level, quorum, tunable-consistency, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "ONE, QUORUM, LOCAL_QUORUM, ALL, ANY"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing consistency levels

Goal: choose a consistency level per query.
- `W + R > RF` gives strong consistency: with RF=3, QUORUM (2 of 3) for both reads and writes overlaps.
- `LOCAL_QUORUM` gives a weaker guarantee within one datacenter; `EACH_QUORUM` needs a majority in every datacenter; `ANY` (writes only) accepts a stored hint as success.
- Writes always go to all replicas; the level only controls how many responses the coordinator waits for.
- `LOCAL_ONE` and `ONE` favour throughput, latency and availability.
Verify: stop one replica in a test and confirm QUORUM reads and writes still succeed.

## Checked

2026-11-02. Checked against the Dynamo architecture page (consistency level list, W+R>RF, QUORUM/LOCAL_QUORUM discussion, writes sent to all replicas). Removed: the cqlsh CONSISTENCY command and driver execution-profile remarks, 'ANY can lose data' wording and the RF=3 tolerance claim (not stated on the page).

Method: documentation only; no commands were run.
