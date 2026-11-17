---
id: computing-software.database-administration.tidb.tidb-tiflash-htap
name: tidb-tiflash-htap
category: computing-software
field: database-administration
product: tidb
tags: [tidb, tiflash, htap, columnar, raft-learner, replication, mpp, analytics]
level: practitioner
status: docs-checked
description: "Understand TiFlash as TiDB's columnar HTAP extension: Raft Learner replication, read consistency, optimizer choice between TiKV and TiFlash, and deployment constraints."
sources: ["https://docs.pingcap.com/tidb/stable/tiflash-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb tiflash htap

TiFlash makes TiDB a hybrid transactional/analytical database. It is a columnar extension of TiKV, with a coprocessor layer efficiently implemented by ClickHouse, and it has its own Multi-Raft system.

Key behaviours:
- Asynchronous replication: TiFlash replicas are Raft Learners, so a TiFlash outage or high latency does not block TiKV writes. Data cannot be written to TiFlash directly; write to TiKV and it replicates over. Replication is per table, and nothing is replicated by default after deployment, so you must create TiFlash replicas for each table.
- Consistency: it gives Snapshot Isolation and reads the latest data. On each read, the TiFlash Region replica sends a lightweight progress-validation request to the Leader, and reads only after replication has caught up to the read timestamp.
- Intelligent choice: the TiDB optimizer picks TiKV (row) or TiFlash (column), or both in one query, based on cost statistics, much as it chooses between indexes.
- Computing acceleration: columnar scans are faster, and TiDB pushes supported computation down to TiFlash. Support is listed in the supported pushdown calculations page.

Deployment notes: Linux AMD64 needs a CPU with AVX2 (check `grep avx2 /proc/cpuinfo`); ARM64 needs ARMv8 with `crc32` and `asimd`. Deploy TiFlash on separate nodes from TiKV for workload isolation; sharing a node is acceptable if you do not need isolation. When you create a replica via DDL, TiDB creates the corresponding placement rules in PD, and PD does the scheduling.

## Checked

2026-11-09: all claims confirmed against the TiFlash Overview page (pingcap/docs tiflash/tiflash-overview.md, read in full). Removed the sentence on MPP mode, which the page only links to.

Method: docs-checked 2026-11-09 against pingcap/docs tiflash/tiflash-overview.md
