---
id: computing-software.data-engineering.databricks.federation-query-pushdown-and-performance
name: federation-query-pushdown-and-performance
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, federation-pushdown, lakehouse-federation, query-performance, foreign-catalogs]
level: advanced
status: docs-checked
description: "Make Lakehouse Federation queries fast: predicate pushdown, reading EXPLAIN FORMATTED, fetch size, parallel JDBC reads and join pushdown limits."
sources:
  - https://docs.databricks.com/aws/en/query-federation/performance-recommendations
  - https://docs.databricks.com/aws/en/query-federation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federation query pushdown and performance

**Goal:** federated queries that move little data from the source database, without overloading the source.

## Predicate pushdown
- Databricks Runtime tries to push predicates to the remote engine. A predicate with no translation (the docs use `ILIKE` against MySQL) is evaluated in Databricks after rows are fetched.
- Join predicates with `AND`: if one part cannot be pushed down, the other part still can, so keep pushable conditions (such as a date comparison) as separate `AND` terms.

## Check it
```sql
EXPLAIN FORMATTED
SELECT * FROM foreign_catalog.schema.table1 t1
INNER JOIN foreign_catalog.schema.table2 t2 ON t1.id = t2.id;
```
`EXPLAIN FORMATTED` shows the query that will run on the remote database (the actual query may differ because of adaptive query execution). A pushed join shows `PushedJoins` and `PushedFilters` in the scan.

## Tuning
- Fetch size: for JDBC-based connectors (Databricks, SQL Server, Azure Synapse, MySQL, Oracle, PostgreSQL, Salesforce Data 360, Teradata) most fetch all data at once by default, which can exceed memory. Setting `fetchSize` makes the connector read in batches (not in parallel). Databricks recommends a large value because very small batches prolong the query. Syntax: `SELECT * FROM mySqlCatalog.schema.table WITH ('fetchSize' 100000)`. Needs Databricks Runtime 16.1 or above, or a Pro or Serverless SQL warehouse.
- Parallel reads (JDBC connectors including Redshift): set `numPartitions`, `partitionColumn`, `lowerBound` and `upperBound` in the `WITH (...)` clause. The bounds only set the partition stride and do not filter rows. Use a numeric, evenly distributed, ideally indexed column. Parallel reads are not supported on a Databricks-created view over a federated table; create the view in the source database instead.
- Snowflake: `partition_size_in_mb` sets the recommended uncompressed partition size; a larger value gives fewer partitions.
- Join pushdown covers Oracle, PostgreSQL, MySQL, SQL Server, Teradata, Redshift, Snowflake and BigQuery. For the first five it is a Public Preview that needs a recent runtime and a toggle on the Previews page; only inner, left-outer and right-outer joins are supported, and a limit, offset or aggregate below the join prevents pushdown. Check the page for current runtime numbers.

## Protect the source
Every federated query runs on the source database: limit who can query foreign catalogs and point the connection at a read replica where you can.

## Verify
`EXPLAIN FORMATTED` shows the filter (and join, where expected) in the pushed query.

## Checked
2026-11-01. Confirmed against the Databricks page "Lakehouse Federation performance recommendations" (predicate pushdown, EXPLAIN FORMATTED, fetchSize, parallel read parameters, Snowflake partition size, join pushdown sources and limits). Removed: the per-connector claims on aggregate, sort and function pushdown, the materialized-view caching example, and the advice on cross-source joins.
Method: documentation only; no commands were run.
