---
id: computing-software.database-administration.cassandra.query-first-modeling
name: query-first-modeling
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, query-first-design, access-patterns, denormalization, data-modeling, partition-key, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Start from queries, one table per query"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/data-modeling_logical.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/data-modeling_rdbms.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/data-modeling_physical.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query-driven table design

Goal: design tables from access patterns.
- List queries first. The docs model with Chebotko notation: conceptual model, query workflow, logical model, physical model.
- Each query gets a table; only equality (or IN) is allowed on a partition key, so queried-by-equality columns go there.
- You cannot join in Cassandra: denormalise into additional tables and manage the copies manually.
- A query that needs `ALLOW FILTERING` may have unpredictable performance.
Verify: every query is served by a table whose primary key matches its restrictions.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: Chebotko notation, denormalisation instead of joins and manual management, partition-key equality rule, `ALLOW FILTERING` caveat (data modeling and DML pages). Removed: the logged-batch recommendation, the clustering-column mapping and the one-partition claim.

Method: documentation only; no commands were run.
