---
id: computing-software.database-administration.tidb.tidb-ticdc-replication
name: tidb-ticdc-replication
category: computing-software
field: database-administration
product: tidb
tags: [tidb, ticdc, changefeed, cdc, kafka, canal-json, avro, debezium, valid-index, redo-log, resolved-ts]
level: advanced
status: docs-checked
description: "Use TiCDC to replicate TiDB changes to TiDB, MySQL, Kafka or object storage, including ordering and consistency guarantees, valid index rules and unsupported scenarios."
sources: ["https://docs.pingcap.com/tidb/stable/ticdc-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb ticdc replication

TiCDC pulls TiKV change logs, sorts them and exports row-based incremental changes through replication tasks called changefeeds. Metadata (node status, changefeed config) is stored in PD's etcd, which provides high availability.

Capabilities: second-level RPO and minute-level RTO between TiDB clusters, bidirectional replication for multi-active setups, low-latency replication to MySQL-compatible databases, Kafka output (Canal-JSON, Avro, Debezium recommended), object storage (S3, GCS, Azure Blob, NFS), filtering by database, table, DML and DDL, and management via Open API.

Guarantees:
- DDL and DML are output at least once. With a MySQL sink, a repeated `CREATE TABLE` fails and is ignored; a repeated `TRUNCATE TABLE` succeeds.
- Kafka sink: distribute rows by table, primary key or timestamp so one row stays in order within a partition. `Resolved TS` messages go to all topics and partitions, meaning everything earlier has been sent; consumers can use it to sort and drop duplicates.
- MySQL sink: single-row update order matches upstream, but downstream transaction order is not guaranteed. Enable redo log for eventual consistency in disasters; the sink URI parameter `transaction-atomicity` (v6.2+) can split large single-table transactions to cut latency and memory.

Valid index: tables need a primary key, or a unique index whose columns are all NOT NULL and not virtual generated columns. `force-replicate` set to `true` forces replication of tables without one.

Unsupported: RawKV-only TiKV, `CREATE SEQUENCE` DDL (DML using sequences still replicates), Lightning physical import into replicated tables, and BR restore into a cluster with replication tasks (relaxed from v8.2.0 when BackupTS precedes the changefeed CheckpointTS).

Best practice: with network latency above 100 ms between clusters, deploy TiCDC near the upstream cluster from v6.5.2 on (near the downstream before that).

## Checked

2026-11-09: capabilities, ordering and consistency guarantees, valid-index rules, unsupported scenarios and the latency best practice confirmed against the TiCDC Overview page (pingcap/docs ticdc/ticdc-overview.md, read in full).

Method: docs-checked 2026-11-09 against pingcap/docs ticdc/ticdc-overview.md
