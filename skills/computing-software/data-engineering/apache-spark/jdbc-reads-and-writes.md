---
id: computing-software.data-engineering.apache-spark.jdbc-reads-and-writes
name: jdbc-reads-and-writes
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-data-sources, spark-jdbc, partitioncolumn, fetchsize, batchsize, numpartitions, pushdown-query, postgres, mysql, sql-server, database-extraction]
level: practitioner
status: docs-checked
description: "Read and write relational databases from Spark via JDBC: parallel reads with partitionColumn bounds, fetchsize, query pushdown, write batching, and not overloading the source."
sources:
  - https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JDBC reads and writes from Spark

**Goal:** pull from or push to an RDBMS in parallel, fast enough, without taking the database down.

## Default read is single-threaded
```python
df = spark.read.jdbc(url, "public.orders", properties=props)   # ONE task, one connection, whole table
```

## Parallel read
```python
df = (spark.read.format("jdbc")
      .option("url", "jdbc:postgresql://<HOST>:5432/shop")
      .option("dbtable", "public.orders")
      .option("user", user).option("password", pwd)          # from a secret store, never literals
      .option("partitionColumn", "order_id")                 # numeric, date or timestamp
      .option("lowerBound", 1).option("upperBound", 50_000_000)
      .option("numPartitions", 16)
      .option("fetchsize", 10000)                           # default 0 = driver default
      .load())
```
- `lowerBound` and `upperBound` only decide the partition stride, not row filtering: all rows in the table are partitioned and returned. They must be given together with `partitionColumn` and `numPartitions`.
- `partitionColumn` must be a numeric, date or timestamp column; an evenly distributed column gives even partitions.
- `numPartitions` also bounds concurrent JDBC connections for reads and writes; agree it with the database owner.
- `fetchsize` (default 0) sets rows per round trip and helps with drivers whose default is low (the docs cite Oracle with 10 rows).

## Push work to the database
```python
.option("query", "SELECT id, status, updated_at FROM orders WHERE updated_at >= '2026-10-15'")
```
`query` and `partitionColumn` cannot be used together; for a parallel read with a subquery, put the subquery in `dbtable` with an alias, for example `(SELECT ... WHERE updated_at >= '...') AS subq`, and qualify the partition column with that alias. The options `pushDownAggregate` and `pushDownLimit` (both default true) control aggregate and LIMIT push-down for the V2 JDBC source.

For custom partitioning use `predicates` (one condition per partition; see the `DataFrameReader.jdbc` API):
```python
preds = [f"created_at >= '{d}' AND created_at < '{d} 23:59:59.999'" for d in days]
spark.read.jdbc(url, "orders", predicates=preds, properties=props)
```

## Writes
```python
(df.repartition(8)                                   # = 8 concurrent connections
   .write.format("jdbc").option("url", url).option("dbtable", "stage.orders_load")
   .option("batchsize", 5000)                         # default 1000 rows per insert round trip
   .option("isolationLevel", "READ_COMMITTED")        # default READ_UNCOMMITTED
   .option("truncate", "true")                       # with overwrite: TRUNCATE instead of DROP/CREATE
   .mode("overwrite").save())
```
- With `overwrite`, `truncate=true` makes Spark truncate the existing table instead of dropping and recreating it, which keeps table metadata such as indices; it will not work in some cases, for example when the new data has a different schema.
- Merge or upsert logic belongs in the database: load into a staging table, then run the database's own merge statement.
- Retried tasks can write a partition more than once, so make the final load idempotent.

## Verify
- [ ] Spark UI shows `numPartitions` tasks for the read stage with similar row counts.
- [ ] The database shows no more concurrent sessions than `numPartitions`.
- [ ] Target row count equals source DataFrame count after the merge step.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/, SQLConf.scala and python/pyspark/sql/readwriter.py on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in sql-data-sources-jdbc.md: partitionColumn types, lowerBound/upperBound stride-only semantics and the option group requirement, fetchsize default 0 (Oracle 10 rows example), batchsize default 1000, isolationLevel default READ_UNCOMMITTED, truncate semantics and caveat, query vs partitionColumn restriction and the dbtable subquery workaround, pushDownAggregate / pushDownLimit defaults. Removed unsourced Postgres fetch and reWriteBatchedInserts claims, the SQL Server connector advice, the 4-16 partition guidance and the claim that Spark has no upsert.

Method: documentation only; no commands were run.
