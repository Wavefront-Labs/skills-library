---
id: computing-software.database-administration.cassandra.node-fails-to-start
name: node-fails-to-start
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, commitlog-replay-failure, port-in-use, system-log-triage, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Boot failures"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing a node that will not start

Goal: find the cause quickly.
- Read `system.log` and `debug.log`; common causes: wrong `listen_address`, port 7000/9042 in use, mismatched cluster name or snitch, corrupt commit log, insufficient file limits.
- Corrupt commit log: move segments aside only if you accept loss and plan repair.
- Never wipe a data directory on a seed without understanding the effect.
Verify: node reaches UN and serves reads.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: storage_port 7000, native_transport_port 9042, listen_address, cluster_name (cassandra.yaml); file limits and vm.max_map_count in the FAQ.
Removed: nothing.
Method: documentation only; no commands were run.
