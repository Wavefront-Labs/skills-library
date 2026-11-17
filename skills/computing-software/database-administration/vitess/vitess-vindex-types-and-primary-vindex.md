---
id: computing-software.database-administration.vitess.vitess-vindex-types-and-primary-vindex
name: vitess-vindex-types-and-primary-vindex
category: computing-software
field: database-administration
product: vitess
tags: [vindex, primary-vindex, secondary-vindex, lookup-vindex, unique, nonunique, functional]
level: practitioner
status: docs-checked
description: "Pick Vitess vindexes: primary versus secondary, unique versus nonunique, functional versus lookup, and what the primary vindex constrains."
sources:
  - https://vitess.io/docs/25.0/reference/features/vindexes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A vindex maps a column value to a keyspace ID, and each shard covers a range of keyspace IDs, so the mapping decides which shard holds a row. Unlike a NoSQL sharding key, a table can have several vindexes, they can be shared by tables, and custom ones are allowed.

Primary vindex: every sharded table must have one; it must be unique (one keyspace ID per input). It decides the target shard on insert, so it defines both the sharding key and the strategy. Column values used by it cannot be updated after insert, since that would move the row to another shard, which Vitess does not support. Unique here does not mean the column is a primary or unique key in MySQL; several rows may share a keyspace ID.

Secondary vindexes let VTGate target only the relevant shards for WHERE clauses that omit the primary vindex; without one the query scatters. They only affect routing, so the shard MySQL instances still need ordinary indexes on those columns.

Unique means at most one keyspace ID per input (lets VTGate push complex queries down when scope is a single shard, and is required for a primary vindex). NonUnique may return several, like a non-unique index.

Functional vindexes compute the keyspace ID by a function (hash or identity) and are typically the primary vindex; the Functional Unique category is the most popular. Lookup vindexes store value-to-keyspace-ID rows in a MySQL table (sharded or unsharded), and are used for lookups by non-primary columns.

## Checked

2026-11-08. Re-read the full Vindexes page (v25.0). Primary and secondary vindex rules, unique versus nonunique, and functional versus lookup definitions confirmed on the Vindexes page.

Method: documentation only; no commands were run.
