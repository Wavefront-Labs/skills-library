---
id: computing-software.database-administration.tidb.tidb-architecture-components
name: tidb-architecture-components
category: computing-software
field: database-administration
product: tidb
tags: [tidb, architecture, tidb-server, pd, tikv, tiflash, htap, distributed-sql, mysql-compatibility]
level: intro
status: docs-checked
description: "Explain TiDB's component layout: stateless TiDB servers, the PD scheduler, TiKV row storage and TiFlash columnar storage, and what each is responsible for."
sources: ["https://docs.pingcap.com/tidb/stable/tidb-architecture"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb architecture components

TiDB is a distributed SQL database built from separate components that communicate with each other.

- TiDB server: a stateless SQL layer that exposes the MySQL protocol endpoint. It parses and optimizes SQL and generates a distributed execution plan. It stores no data, is horizontally scalable, and is normally fronted by a load balancer such as TiProxy, LVS, HAProxy, ProxySQL or F5.
- Placement Driver (PD): the metadata manager and "brain" of the cluster. It stores real-time data distribution for every TiKV node and the cluster topology, serves the TiDB Dashboard UI, allocates transaction IDs, and sends scheduling commands to TiKV nodes. It runs at least three nodes for high availability; an odd number of PD nodes is recommended.
- TiKV: the distributed transactional key-value storage engine. The Region is the basic storage unit, covering a key range from StartKey (inclusive) to EndKey (exclusive). TiKV offers native distributed transactions at key-value level with Snapshot Isolation by default; data is automatically kept in multiple replicas (three by default).
- TiFlash: a special storage server that stores data by column, mainly to accelerate analytical queries.

Advertised properties: elastic scalability, MySQL protocol and syntax compatibility (often with no application code change), automatic failover when a minority of replicas fail, and ACID transactions with strong consistency.

## Checked

2026-11-09: component roles, Region definition, default Snapshot Isolation, three default replicas, PD node count and the advertised properties confirmed against the TiDB Architecture page (pingcap/docs tidb-architecture.md). Removed the unsourced troubleshooting mental-model paragraph.

Method: docs-checked 2026-11-09 against pingcap/docs tidb-architecture.md (read in full)
