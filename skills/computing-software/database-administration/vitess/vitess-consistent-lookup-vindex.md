---
id: computing-software.database-administration.vitess.vitess-consistent-lookup-vindex
name: vitess-consistent-lookup-vindex
category: computing-software
field: database-administration
product: vitess
tags: [vindex, lookup-vindex, consistent-lookup, owner-table, two-phase-commit, shared-vindex]
level: advanced
status: docs-checked
description: "Design lookup vindex tables and choose consistent_lookup over lookup in Vitess: owner tables, the pre, normal and post sessions, table layout, and the same-transaction limitation."
sources:
  - https://vitess.io/docs/25.0/reference/features/vindexes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A lookup vindex is populated through an owner table: inserting a row into the owner creates the lookup row, and deleting removes it. With a plain lookup vindex this is a distributed transaction across shards. Consistent lookup vindexes (`consistent_lookup_unique` and `consistent_lookup`) instead use careful locking and transaction ordering to stay consistent without 2PC.

VTGate may open three sessions: pre, normal and post. Lookup queries use pre and post; the original client query uses normal. For an insert, the lookup insert goes via the pre session and the row insert via normal; commit runs pre first, then post. For update or delete, the lookup change uses the post session; commit runs normal first, then post. A lock is taken whenever a consistent lookup is involved. Limitation: an insert followed by an update or delete in the same transaction for the same consistent lookup column value is not supported.

Migration: a `lookup_unique` can be switched to `consistent_lookup_unique` by changing the type in the VSchema because the data is compatible. A `lookup` can become `consistent_lookup` only if the `from` columns uniquely identify the owner row. Vitess does not cascade deletes from the owner table.

Table layout: two columns, a `from` column matching the main table's column type and a `to` column that is BINARY or VARBINARY large enough for the keyspace ID. For non-unique lookups add the columns that identify the owner row, usually its primary key; for user rows (user_id, email) the table is `(email, user_id, keyspace_id)`. Foreign-key-related tables can share one lookup vindex, with one table designated owner. Functional vindexes can be shared but have no owner.

## Checked

2026-11-08. Re-read the full Vindexes page (v25.0). Consistent lookup types, session behaviour, limitation, conversion rules, table layout and shared vindexes confirmed on the Vindexes page.

Method: documentation only; no commands were run.
