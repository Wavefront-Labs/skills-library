---
id: computing-software.database-administration.schema-design.audit-and-history-tables
name: audit-and-history-tables
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, schema-patterns, audit-table, history-table, audit-trigger, temporal-tables, system-versioning, change-data-capture, row-history]
level: advanced
status: gated
description: "Record who changed what and when: trigger-based audit tables, SQL:2011 system-versioned temporal tables, and CDC, with their trade-offs in storage and reliability."
sources:
  - https://wiki.postgresql.org/wiki/Audit_trigger
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
  - https://mariadb.com/kb/en/system-versioned-tables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit and history tables

**Goal:** answer "what did this row look like last Tuesday, and who changed it?"
without trusting application code to remember to log.

## Option 1: trigger-based audit table (any engine)
```sql
CREATE TABLE audit_log (
  id bigserial PRIMARY KEY,
  table_name text NOT NULL, row_pk text NOT NULL,
  action char(1) NOT NULL CHECK (action IN ('I','U','D')),
  changed_at timestamptz NOT NULL DEFAULT now(),
  changed_by text NOT NULL DEFAULT coalesce(current_setting('app.user', true), 'unknown'),
  old_row jsonb, new_row jsonb);

CREATE FUNCTION audit_trg() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO audit_log(table_name,row_pk,action,old_row,new_row)
  VALUES (TG_TABLE_NAME,
          COALESCE(NEW.id, OLD.id)::text, left(TG_OP,1),
          CASE WHEN TG_OP <> 'INSERT' THEN to_jsonb(OLD) END,
          CASE WHEN TG_OP <> 'DELETE' THEN to_jsonb(NEW) END);
  RETURN NULL;
END $$;
CREATE TRIGGER orders_audit AFTER INSERT OR UPDATE OR DELETE ON orders
  FOR EACH ROW EXECUTE FUNCTION audit_trg();
```
Pass the end user (not the pooled DB role) per transaction with `SELECT set_config('app.user', 'alice', true)`. `SET LOCAL app.user = 'alice'` is a syntax error because `user` is a reserved word (use `SET LOCAL "app.user"` or a different name such as `app.username`). `current_setting('app.user', true)` returns NULL when the setting was never defined in the session, which would violate NOT NULL without the coalesce above (run on PostgreSQL 18).
Cost: extra write per change in the same transaction (reliable, but slower writes).

## Option 2: system-versioned temporal tables
SQL Server 2016+ (Microsoft's temporal-tables page lists SQL Server 2016 and later), MariaDB (see its system-versioned tables docs for the first version) and others: the engine keeps a history table with
validity periods and supports time-travel queries.
```sql
-- SQL Server (not run here: no SQL Server available; gated: unconfirmed, source is paywalled or blocked))
ALTER TABLE dbo.orders ADD
  valid_from datetime2 GENERATED ALWAYS AS ROW START HIDDEN NOT NULL DEFAULT SYSUTCDATETIME(),
  valid_to   datetime2 GENERATED ALWAYS AS ROW END HIDDEN NOT NULL DEFAULT '9999-12-31',
  PERIOD FOR SYSTEM_TIME (valid_from, valid_to);
ALTER TABLE dbo.orders SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.orders_history));
SELECT * FROM dbo.orders FOR SYSTEM_TIME AS OF '2026-10-13T09:00:00';
```
Stores "what", not "who": add a `modified_by` column maintained by the app or trigger.
PostgreSQL has no native support (extensions like `temporal_tables`/periods exist).

## Option 3: CDC to an external store
Debezium/logical decoding or SQL Server CDC streams changes to Kafka/a
warehouse: no write overhead in the transaction, but asynchronous and depends
on the pipeline being healthy. Good for analytics history, weaker as a legal audit trail.

## Gotchas
- History grows without bound: partition by time and define retention.
- Bulk updates multiply audit volume; a mass backfill can write millions of audit rows.
- Schema changes to the base table must be applied to history tables too
  (temporal tables handle this; triggers with jsonb are tolerant).
- Restrict UPDATE/DELETE on audit tables (grant INSERT only) so the trail is append-only.

## Verify
Update a row and query the history for its previous version, with the correct user and timestamp.
