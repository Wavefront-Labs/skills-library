---
id: computing-software.database-administration.cassandra.query-tracing-and-slow-logs
name: query-tracing-and-slow-logs
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, query-tracing, tracing-probability, slow-query-log, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Diagnosing single queries"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracing and slow query logging

Goal: find slow queries.
- `TRACING ON;` in cqlsh shows steps per replica; `nodetool settraceprobability` samples queries; traces are kept in the `system_traces` keyspace.
- Full query logging (`fqltool`) and audit logging are documented under managing/operating.
- Look for tombstone scans, high SSTable counts, cross-DC hops.
Verify: trace shows the expected replica count.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: TRACING ON in cqlsh, settraceprobability command (nodetool source), system_traces, fqltool and audit logging pages.
Removed: the 0.001 value and 4.x version claim.
Method: documentation only; no commands were run.
