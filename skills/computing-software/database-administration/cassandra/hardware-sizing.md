---
id: computing-software.database-administration.cassandra.hardware-sizing
name: hardware-sizing
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, node-sizing, jbod, disk-capacity, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Capacity planning"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardware sizing and disk layout

Goal: size nodes.
- Hardware guide: ECC RAM; heap no less than 2GB and no more than 50% of RAM.
- Use separate disks for commit log and data; with JBOD set `disk_failure_policy`.
- Size per-node data and free space from your own streaming and compaction times.
Verify: replacement-node bootstrap time fits your RTO.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: ECC RAM, heap bounds (hardware page), disk_failure_policy (cassandra.yaml).
Removed: the 1-2 TB and free-space percentages.
Method: documentation only; no commands were run.
