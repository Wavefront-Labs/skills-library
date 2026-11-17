---
id: computing-software.database-administration.postgresql.logical-replication-restrictions-and-replica-identity
name: logical-replication-restrictions-and-replica-identity
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, logical-replication-restrictions, replica-identity, logical-replication, ddl-replication, sequences, large-objects]
level: practitioner
status: verified
description: "Plan around PostgreSQL logical replication limits: no DDL, sequences or large objects, and set REPLICA IDENTITY so UPDATE/DELETE replicate."
sources:
  - https://www.postgresql.org/docs/current/logical-replication-restrictions.html
  - https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-REPLICA-IDENTITY
  - https://www.postgresql.org/docs/current/logical-replication-publication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logical replication restrictions and REPLICA IDENTITY

## Not replicated
| Thing | Consequence | Workaround |
|---|---|---|
| DDL (CREATE/ALTER/DROP) | subscriber errors when a column appears in the stream it does not have | apply DDL on the subscriber **first** for additive changes, then the publisher; for drops, publisher first |
| Sequence values | subscriber sequences stay at their start value; after cutover inserts collide | before cutover copy `last_value` + margin with `setval()` (sequence synchronisation, `FOR ALL SEQUENCES` and `REFRESH SEQUENCES`, appears only in the PostgreSQL development docs, not in 18) |
| Large objects (`pg_largeobject`) | silently missing | migrate to bytea, or copy LOs separately |
| TRUNCATE | replicated since PG11 (can be excluded with `publish`) | — |
| Views, materialized views, foreign tables | not replicable | refresh/recreate on subscriber |

Also: tables are matched by schema-qualified name; column types must be compatible (text-convertible); partitioned tables need `publish_via_partition_root` when the subscriber's partitioning differs.

## REPLICA IDENTITY
UPDATE and DELETE need a way to identify the old row on the subscriber.
```sql
SELECT relname, relreplident FROM pg_class WHERE relnamespace = 'public'::regnamespace AND relkind IN ('r','p');
-- d = default (primary key), i = index, f = full, n = nothing
```
- Table with a PK: default works.
- No PK but a unique NOT NULL index: `ALTER TABLE t REPLICA IDENTITY USING INDEX t_uniq_idx;`
- Neither: `ALTER TABLE t REPLICA IDENTITY FULL;` — the whole old row is logged; WAL grows and the subscriber searches by all columns (seq scan per row unless an index exists; PG16 can use a suitable index).
- `NOTHING` plus a table in a publication that publishes update/delete: the UPDATE fails on the **publisher** with `cannot update table "t" because it does not have a replica identity and publishes updates`.

Find tables that will break:
```sql
SELECT c.oid::regclass FROM pg_class c
WHERE c.relkind = 'r' AND c.relnamespace NOT IN ('pg_catalog'::regnamespace, 'information_schema'::regnamespace)
  AND c.relreplident = 'd'
  AND NOT EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = c.oid AND i.indisprimary);
```

## Pre-flight checklist
1. Every published table has PK or explicit replica identity.
2. Schema (DDL) applied on subscriber: `pg_dump --schema-only` restore.
3. Sequence sync step in the cutover runbook.
4. No large objects (`SELECT count(*) FROM pg_largeobject_metadata;` = 0).

## Gotchas
- Subscriber-side triggers fire only if `ALTER TABLE ... ENABLE REPLICA TRIGGER` / `ENABLE ALWAYS TRIGGER`. The apply worker runs with an empty `search_path`, so trigger functions must schema-qualify every object (tested: an unqualified `insert into trg_log` failed with `relation "trg_log" does not exist` and stalled replication of that table).
- Generated columns: not replicated before PG18 (18 adds the `publish_generated_columns` publication option); the subscriber computes its own.

## Checked
- PostgreSQL 17.6 publisher and subscriber: DDL not replicated (apply error on a missing column), a sequence used by a published table stays at its start on the subscriber (`last_value` 1, `is_called` false against 3), `TRUNCATE` replicated, a large object not replicated, a view cannot be published (`cannot add relation "v1" to publication`), a generated column was recomputed on the subscriber, `relreplident` and the broken-table checklist query run (`d`, `f`, `i` states; `i` with a unique NOT NULL index lets updates through, default without a key fails with the quoted publisher error), and a replica trigger fired in the apply worker. Release notes: TRUNCATE replication in 11, generated-column publishing in 18; the 18 and devel docs show sequence sync only in devel.
