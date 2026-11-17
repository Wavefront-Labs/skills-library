---
id: computing-software.database-administration.cassandra.sai-index-creation
name: sai-index-creation
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, sai-queries, sai-index-options, vector-search, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "SAI in Cassandra 5"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/cql_singlefile.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/indexing/sai/sai-faq.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/indexing/sai/sai-concepts.html", "https://cassandra.apache.org/doc/latest/cassandra/architecture/storage-engine.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage-Attached Index setup

Goal: add flexible predicate queries.
- `CREATE INDEX ON users (age) USING 'sai';` (example from the CQL docs). SAI supports equality and range queries on numeric and non-literal types, and equality and non-exact matching on strings.
- An index can be created before data is written or after.
- SAI writes its own components alongside each SSTable (`SAI*.db`) and builds them during flush and compaction.
- `sai_indexes_per_table_failure_threshold` in cassandra.yaml caps SAI indexes per table (10 by default).
Verify: tracing shows index use.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: `USING 'sai'` syntax, supported query types, creation timing, `SAI*.db` components, the per-table index limit (CQL reference, SAI FAQ and concepts, storage engine). Removed: text-analyzer options and the vector index claim (not confirmed).

Method: documentation only; no commands were run.
