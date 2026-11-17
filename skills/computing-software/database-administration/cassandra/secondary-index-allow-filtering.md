---
id: computing-software.database-administration.cassandra.secondary-index-allow-filtering
name: secondary-index-allow-filtering
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, secondary-index, sai-vs-2i, index-selection, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "When indexes help and when to denormalise"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/indexing/indexing-concepts.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/indexing/sai/sai-faq.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/cql_singlefile.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secondary indexes and ALLOW FILTERING

Goal: choose an index or a new table.
- Classic secondary indexes are local indexes stored in a hidden table on each node; the docs recommend them only in conjunction with a partition key.
- SAI is the newer index (`CREATE INDEX ... USING 'sai'`); its FAQ discusses column cardinality and read performance.
- A query using `ALLOW FILTERING` may have unpredictable performance; avoid it on large tables.
Verify: tracing shows the query touching few nodes.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: classic index behaviour and recommendation, SAI syntax and cardinality FAQ, `ALLOW FILTERING` caveat. Removed: the cardinality and counter rules for classic indexes and the 5.0 version claim.

Method: documentation only; no commands were run.
