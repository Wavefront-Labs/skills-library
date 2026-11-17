---
id: computing-software.database-administration.cassandra.static-columns-and-collections
name: static-columns-and-collections
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, static-column, collections, frozen-types, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Per-partition values and nested types"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/cql_singlefile.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/types.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/ddl.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static columns, collections, frozen types

Goal: model per-partition and nested values.
- A `STATIC` column is shared by all rows of the same partition.
- Collections are meant for denormalising a relatively small amount of data; use a table with clustering columns when the data grows unbounded.
- Single elements or fields can be updated on non-frozen collections and UDTs (`id[value]`, `id.field`); an INSERT always replaces an entire list.
- `WRITETIME` and `TTL` cannot be used on multi-cell columns such as non-frozen collections. UDTs are created with `CREATE TYPE`.
Verify: `DESCRIBE KEYSPACE` output shows the static and frozen markers as intended.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: STATIC columns, collection sizing guidance, element and field updates, WRITETIME/TTL limit (CQL reference, types page). Removed: the 'few hundred items' figure, the frozen-as-one-blob wording and the range tombstone claim.

Method: documentation only; no commands were run.
