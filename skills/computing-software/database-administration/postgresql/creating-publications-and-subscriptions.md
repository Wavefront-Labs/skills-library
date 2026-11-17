---
id: computing-software.database-administration.postgresql.creating-publications-and-subscriptions
name: creating-publications-and-subscriptions
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, logical-replication, create-publication, create-subscription, copy-data, tablesync, replication-slots]
level: practitioner
status: verified
description: "Set up PostgreSQL logical replication end to end: wal_level, schema copy, CREATE PUBLICATION/SUBSCRIPTION, initial copy, adding tables later and teardown."
sources:
  - https://www.postgresql.org/docs/current/logical-replication-quick-setup.html
  - https://www.postgresql.org/docs/current/sql-createpublication.html
  - https://www.postgresql.org/docs/current/sql-createsubscription.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating publications and subscriptions

## Publisher prerequisites
```sql
ALTER SYSTEM SET wal_level = logical;       -- restart required
SHOW max_replication_slots; SHOW max_wal_senders;   -- one slot + sender per subscription (+ tablesync)
CREATE ROLE repl_user LOGIN REPLICATION PASSWORD '...';
GRANT SELECT ON ALL TABLES IN SCHEMA app TO repl_user;   -- needed for the initial copy
```
pg_hba.conf: logical replication connects to a **normal database name**, not `replication`:
`hostssl app repl_user 10.0.2.0/24 scram-sha-256`.

Every published table that receives UPDATE/DELETE needs a primary key or a
`REPLICA IDENTITY` (`USING INDEX` on a unique not-null index, or `FULL`), otherwise those
statements **fail on the publisher**.

## Schema on the subscriber
Logical replication does not copy DDL:
```bash
pg_dump -h pub -d app --schema-only -n app | psql -h sub -d app
```

## Create
```sql
-- publisher
CREATE PUBLICATION app_pub FOR TABLES IN SCHEMA app;     -- PG15+; or FOR TABLE t1, t2; or FOR ALL TABLES
-- subscriber
CREATE SUBSCRIPTION app_sub
  CONNECTION 'host=pub dbname=app user=repl_user password=... sslmode=verify-full'
  PUBLICATION app_pub
  WITH (copy_data = true, streaming = parallel, disable_on_error = true);
```
The subscription creates a slot on the publisher, then **tablesync workers** copy each table
(`max_sync_workers_per_subscription`, default 2), then streams changes from the slot.

## Adding tables later
```sql
ALTER PUBLICATION app_pub ADD TABLE app.new_table;        -- publisher (automatic with IN SCHEMA)
-- create the table on the subscriber first, then:
ALTER SUBSCRIPTION app_sub REFRESH PUBLICATION;           -- starts its initial copy
```

## Options worth knowing
- `copy_data = false` when the subscriber already has the data (e.g. restored from a
  backup at a known LSN) to avoid duplicates.
- `create_slot = false, slot_name = 'x'` to use a pre-created slot.
- `binary = true` faster copy/apply when types match on both sides.
- `origin = none` (PG16) for bidirectional setups to avoid loops.
- `disable_on_error = true` stops the apply worker on conflict instead of retrying forever.

## Teardown
```sql
DROP SUBSCRIPTION app_sub;      -- also drops the remote slot if it can connect
```
If the publisher is gone: `ALTER SUBSCRIPTION app_sub DISABLE; ALTER SUBSCRIPTION app_sub SET (slot_name = NONE); DROP SUBSCRIPTION app_sub;`
and drop the orphaned slot on the publisher if it comes back, or it retains WAL forever.

## Verify
```sql
SELECT s.subname, r.srrelid::regclass, r.srsubstate FROM pg_subscription_rel r
  JOIN pg_subscription s ON s.oid = r.srsubid;                      -- r = ready (there is no regsubscription type)
SELECT subname, received_lsn, latest_end_lsn, last_msg_receipt_time FROM pg_stat_subscription;
```
All tables in state `r`, row counts match, and a test insert appears on the subscriber.
Sequences are not replicated: sync them before cutover.

## Checked
- Two local PostgreSQL 17.6 instances (publisher with `wal_level=logical`, subscriber on another port): `FOR TABLES IN SCHEMA` publication, schema-only `pg_dump` piped to the subscriber, `CREATE SUBSCRIPTION ... (copy_data, streaming = parallel, disable_on_error)` created the slot and copied all tables (`pg_subscription_rel` states `r`; `srsubid::regsubscription` fails with `type "regsubscription" does not exist`, so the query now joins `pg_subscription`); `pg_stat_subscription` has the listed columns; an `UPDATE` on a published table without replica identity fails on the publisher with the quoted error and `REPLICA IDENTITY USING INDEX` fixes it; adding a column only on the publisher made the apply worker fail with `target relation ... is missing replicated column` and `disable_on_error` disabled the subscription until the column existed on the subscriber and it was re-enabled; `REFRESH PUBLICATION` is refused on a disabled subscription; `binary`, `origin = none`, `failover = true` are accepted (release notes: `TABLES IN SCHEMA` and `disable_on_error` in 15, `origin` and parallel streaming in 16, failover in 17); `DROP SUBSCRIPTION` dropped the remote slot, while the slot of a subscription detached with `slot_name = NONE` stayed on the publisher.
