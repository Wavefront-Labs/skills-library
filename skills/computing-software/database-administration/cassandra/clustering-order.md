---
id: computing-software.database-administration.cassandra.clustering-order
name: clustering-order
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, clustering-order, order-by, time-series-table, clustering-columns, primary-key, compound-key, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "CLUSTERING ORDER BY and range slices"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clustering columns and sort order

Goal: store rows pre-sorted for range reads.
- `WITH CLUSTERING ORDER BY (ts DESC)` serves "latest N" with `LIMIT N` and no sort.
- `ORDER BY` is limited to the table clustering order or its reverse.
Verify: `SELECT ... LIMIT 10` returns newest first with no ALLOW FILTERING.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: CLUSTERING ORDER BY syntax and default ascending, ORDER BY limited to the clustering order or its reverse (ddl and dml pages).
Removed: the clustering-column restriction rule.
Method: documentation only; no commands were run.
