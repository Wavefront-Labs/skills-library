---
id: computing-software.database-administration.cassandra.spark-connector-usage
name: spark-connector-usage
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, spark-connector, dataframe-cassandra, join-with-cassandra-table, spark-cassandra-connector, analytics-workloads, dc-isolation, nosql, wide-column, cql]
level: practitioner
status: draft
description: "Batch analytics"
sources: ["https://cassandra.apache.org/doc/latest/", "https://docs.datastax.com/en/cql/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spark Cassandra Connector

Goal: analyse Cassandra data safely.
- Read with `spark.read.format("org.apache.spark.sql.cassandra").options(table="t", keyspace="ks")`.
- Pushdown of partition-key predicates; avoid full scans on hot tables.
- Use `joinWithCassandraTable` for key lookups.
Verify: Spark reads token ranges in parallel with no timeouts.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
