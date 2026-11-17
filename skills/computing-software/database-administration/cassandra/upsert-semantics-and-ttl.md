---
id: computing-software.database-administration.cassandra.upsert-semantics-and-ttl
name: upsert-semantics-and-ttl
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, upsert, using-ttl, writetime, cql-dml, insert, select, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Writes are upserts"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/cql_singlefile.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upserts, TTL and write timestamps

Goal: write correct mutations.
- INSERT does not check whether the row exists: it is created if none existed and updated otherwise.
- `USING TTL 3600 AND TIMESTAMP <micros>`: TTL is in seconds and applies to the inserted values (a later update resets it); the default timestamp is the coordinator time in microseconds.
- Columns omitted from an INSERT JSON default to NULL, which creates a tombstone; `DEFAULT UNSET` leaves them alone.
- `WRITETIME(col)` and `TTL(col)` can be selected to inspect metadata (not on multi-cell columns).
Verify: TTL(col) counts down after insert.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: upsert behaviour, TTL and TIMESTAMP units, JSON NULL/UNSET defaults, WRITETIME/TTL selectors (DML page, CQL reference). Removed: the row-marker explanation (not found in the pages).

Method: documentation only; no commands were run.
