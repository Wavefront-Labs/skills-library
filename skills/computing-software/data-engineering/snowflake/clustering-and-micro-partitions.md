---
id: computing-software.data-engineering.snowflake.clustering-and-micro-partitions
name: clustering-and-micro-partitions
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, micro-partitions, clustering-key, clustering-depth, automatic-clustering, partition-pruning, system-clustering-information, query-pruning, reclustering-credits, metadata-pruning, snowflake-pruning]
level: advanced
status: docs-checked
description: "Understand Snowflake micro-partitions and clustering keys to fix pruning on large tables without over-applying clustering."
sources:
  - https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions
  - https://docs.snowflake.com/en/user-guide/tables-clustering-keys
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Snowflake micro-partitions and clustering — when to intervene and when not to

**Goal:** fix a specific, measured pruning problem on a genuinely large table without reflexively adding clustering keys to every table and paying for reclustering that never pays for itself. (Complements computing-software.data-engineering.data-warehouse-architecture.partitioning-and-clustering-strategy, which covers the cross-platform decision; this is Snowflake's specific mechanics.)

## 1. What a micro-partition actually is
Snowflake automatically divides every table into micro-partitions (50 to 500 MB before compression) as data is inserted or loaded, and records metadata about the rows in each one. A query's `WHERE` clause lets Snowflake **prune** (skip without reading) micro-partitions that cannot match the filter. Pruning happens on every table with no clustering key set, based on the natural order the data landed in. A naturally time-ordered table (daily loads appended) often already prunes well on a date filter, so measure pruning (section 3) before assuming a clustering key is needed.

## 2. When a clustering key is actually warranted
Per the docs, a clustering key co-locates data in the same micro-partitions and is useful for very large tables where the ordering was not ideal when the data was loaded, or where extensive DML has degraded the table's natural clustering. Snowflake's own guidance: consider it when the table has a large number of micro-partitions (typically multiple terabytes), queries filter or sort on the same few columns, and the improved query performance offsets the credits needed to cluster and maintain the table. Queries on a small or medium table rarely repay that cost.

Defining the key is `ALTER TABLE t CLUSTER BY (col1, col2)` (or `CLUSTER BY` in `CREATE TABLE`). After that, maintenance is automatic (Automatic Clustering): rows are not necessarily reordered immediately, and Snowflake only reclusters when the table will benefit.

## 3. Measuring before (and after) touching clustering
```sql
SELECT SYSTEM$CLUSTERING_INFORMATION('my_table', '(order_date)');
```
This calculates clustering details, including clustering depth, and can be run on any columns of any table, whether or not the table has an explicit clustering key. Use it to judge whether pruning on the filtered column is already good enough, and compare it with how a specific slow query behaves; a slow query is the real test, not an abstract depth number in isolation.

## 4. Cost and behaviour
Reclustering consumes credits like any other DML in Snowflake; the amount depends on the size of the table and the amount of data that has to be reclustered. A table loaded out of order against a tight key can therefore carry a permanent cost line. Compare the credits spent against the query-time savings before keeping the key (look up the Automatic Clustering cost and history views in the Snowflake docs for where to read the credits).
- A clustering key can be removed (`ALTER TABLE t DROP CLUSTERING KEY`) if the cost does not justify the benefit.
- A cloned table keeps the clustering key, but Automatic Clustering is suspended for the clone and must be resumed.

## 5. Choosing the key (from the docs)
- Cluster on columns most actively used in selective filters or joins; columns used in `GROUP BY` or `ORDER BY` are usually less helpful, so favour filter and join columns.
- Cardinality matters. A very low-cardinality column (a Boolean) gives little pruning; a very high-cardinality column (nanosecond timestamps, unique ids) is expensive to maintain and typically a poor key. To use a high-cardinality column, use an expression that preserves ordering and cuts distinct values, for example `TO_DATE(c_timestamp)`.
- The cost of clustering on a unique key may exceed its benefit, especially if point lookups are not the table's main use.
- Snowflake recommends at most 3 or 4 columns (or expressions) per key for most tables, and ordering them from lowest cardinality to highest; a higher-cardinality column placed first reduces the effectiveness of clustering on the later ones.
- For text columns, key metadata tracks only the first several bytes (typically 5 or 6), which can be fewer than 5 characters in multi-byte character sets.

## Common mistake
Assuming clustering fixes a query that is slow for another reason (a bad join, an undersized warehouse). Confirm the cost is in scanning too many micro-partitions before reaching for a clustering key.

## Verify
- [ ] `SYSTEM$CLUSTERING_INFORMATION` and a representative slow query were examined before adding a clustering key.
- [ ] Key columns are those used in selective filters or joins, at most 3 or 4, ordered lowest to highest cardinality.
- [ ] Reclustering credit consumption was reviewed after a few weeks and compared with query-time improvement.
- [ ] No key on a unique or nanosecond-precision column without an ordering-preserving expression.

## Checked
2026-11-09. Confirmed against the Snowflake docs "Micro-partitions and data clustering" and "Clustering keys and clustered tables": 50 to 500 MB uncompressed size, automatic pruning, multi-TB guidance, SYSTEM$CLUSTERING_INFORMATION on any table, credit cost of reclustering, DROP CLUSTERING KEY, the 3 or 4 column recommendation, lowest-to-highest cardinality ordering, text key length, and the clone behaviour. Removed or corrected: "immutable", the cloud services metadata layer detail, "billed as its own service", the AUTOMATIC_CLUSTERING_HISTORY and query-profile specifics (not on the pages read), and the earlier advice to put the most selectively filtered column first, which contradicts the documented cardinality ordering.
Method: documentation only; no commands were run.
