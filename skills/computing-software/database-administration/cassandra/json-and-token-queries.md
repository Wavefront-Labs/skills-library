---
id: computing-software.database-administration.cassandra.json-and-token-queries
name: json-and-token-queries
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, select-json, insert-json, token-function, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "JSON and token range scans"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON support and token() queries

Goal: use JSON and partition scans appropriately.
- `INSERT INTO t JSON '{"id":1,"name":"x"}'`, `SELECT JSON * FROM t`.
- `WHERE token(pk) > ? AND token(pk) <= ?` paginates a full scan by token range.
- Use driver paging for scans rather than guessing LIMITs.
Verify: token-range scans cover each row exactly once on a test table.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: INSERT JSON and SELECT JSON (JSON support page), token() semantics (functions and dml pages).
Removed: nothing.
Method: documentation only; no commands were run.
