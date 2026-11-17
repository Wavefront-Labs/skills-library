---
id: computing-software.database-administration.clickhouse.distributed-tables-and-sharding
name: distributed-tables-and-sharding
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, sharding, distributed, shards, on-cluster, insert-routing]
level: practitioner
status: docs-checked
description: "Split ClickHouse data across shards with a Distributed table, covering ON CLUSTER DDL, insert routing by sharding key and SELECT forwarding."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/managing-data/core-concepts/shards.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# distributed tables and sharding
In traditional shared-nothing clusters, sharding is used when the data is too large for one server or one server is too slow. Each shard holds a subset of the data and is a regular table that can be queried independently, but a query on it only sees that subset. A Distributed table gives a unified view: it stores no data, forwards SELECTs to all shards, assembles the results and routes INSERTs.
```sql
CREATE TABLE uk.uk_price_paid_simple_dist ON CLUSTER test_cluster
(
    date Date,
    town LowCardinality(String),
    street LowCardinality(String),
    price UInt32
)
ENGINE = Distributed('test_cluster', 'uk', 'uk_price_paid_simple', rand())
```
`ON CLUSTER` makes the DDL a distributed DDL statement run on all servers in the cluster definition; it needs a Keeper component. The engine parameters are the cluster name, the database and table of the sharded target, and the sharding key.

INSERT routing: for each row ClickHouse evaluates the sharding key (here `rand()`, random assignment; any expression can be used), takes the result modulo the number of shard servers, and uses it as the target server ID (starting at 0). SELECT forwarding: the Distributed table forwards the query to all shard servers, each computes its local result in parallel, and the initially targeted server merges them into the final result.

Replicas (copies of a shard, which also require Keeper): the Distributed table forwards a SELECT to one replica per shard; by default it prefers a local replica, and other load-balancing strategies can be configured. This topic does not apply to ClickHouse Cloud, where parallel replicas act like shards and object storage replaces replicas.

## Checked
2026-11-03. Confirmed against the "Table shards and replicas" page. Removed: "local table must exist first", the sharding-key skew and cross-shard join gotchas, the "column hash keeps related rows together" claim, and the count()/`hostName()` Verify step, none of which are on the page.
Method: documentation only; no commands were run.
