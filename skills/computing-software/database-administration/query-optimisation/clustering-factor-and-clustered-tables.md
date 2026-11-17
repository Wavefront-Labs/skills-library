---
id: computing-software.database-administration.query-optimisation.clustering-factor-and-clustered-tables
name: clustering-factor-and-clustered-tables
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, clustering-factor, clustered-index, index-organized-table, cluster-command, indexing]
level: practitioner
status: draft
description: "Understand clustering factor (how table row order matches an index) and clustered or index-organized tables, and how they decide whether index range scans are cheap."
sources:
  - https://use-the-index-luke.com/sql/clustering
  - https://www.postgresql.org/docs/current/sql-cluster.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/tgsql/optimizer-access-paths.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clustering factor and clustered / index-organized tables

## Why two identical indexes perform differently
An index range scan finds row pointers in order, then fetches table rows. If matching rows sit together in few table blocks, the fetch is cheap; if they are scattered, each row costs a random block read. The **clustering factor** measures this: close to the number of table blocks = well clustered; close to the number of rows = scattered.

## Seeing it
- Oracle: `SELECT index_name, clustering_factor, num_rows, (SELECT blocks FROM user_tables WHERE table_name='ORDERS') blocks FROM user_indexes WHERE table_name='ORDERS';`
- PostgreSQL: `pg_stats.correlation` per column (-1..1); near ±1 = physical order matches; near 0 = scattered. Affects index scan vs bitmap scan costing.
- SQL Server/MySQL InnoDB: tables *are* clustered on the clustered index/primary key, so the question becomes "is this a clustered index range or a secondary index with lookups?"

## Clustered / index-organized storage
| Engine | Storage |
|---|---|
| InnoDB | Always clustered by PRIMARY KEY; secondary indexes store the PK |
| SQL Server | Clustered index (usually PK) or heap |
| Oracle | Heap by default; IOT (`ORGANIZATION INDEX`) optional |
| PostgreSQL | Heap only; `CLUSTER` reorders once, not maintained |
| SQLite | rowid B-tree (clustered on rowid); WITHOUT ROWID clusters on PK |

Design consequences:
- Choose the clustered key to match the most important range access (`(customer_id, order_date)` for "orders of a customer"), keep it narrow and ever-increasing to limit page splits (InnoDB/SQL Server secondary indexes carry it).
- Random UUID primary keys in InnoDB/SQL Server scatter inserts and destroy locality: use time-ordered keys (UUIDv7, sequential) for clustered keys.

## Improving clustering in PostgreSQL
- `CLUSTER orders USING idx_orders_customer;` rewrites the table in index order (ACCESS EXCLUSIVE lock); `pg_repack --order-by` does it online. Order decays with updates; repeat periodically for append-mostly tables.
- Use covering indexes (`INCLUDE`) and index-only scans to avoid the table fetch altogether.
- BRIN indexes rely on natural correlation (time-ordered inserts).

## Verify
Compare buffers read for the same range query before and after (`EXPLAIN (ANALYZE, BUFFERS)`); `pg_stats.correlation` close to 1 after CLUSTER.
