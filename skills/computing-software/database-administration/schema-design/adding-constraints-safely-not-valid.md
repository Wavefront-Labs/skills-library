---
id: computing-software.database-administration.schema-design.adding-constraints-safely-not-valid
name: adding-constraints-safely-not-valid
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, schema-migration, expand-contract, not-valid-constraint, validate-constraint, with-nocheck, zero-downtime]
level: advanced
status: gated
description: "Add foreign keys, CHECK and NOT NULL constraints to large live tables without long locks: NOT VALID then VALIDATE in PostgreSQL, WITH NOCHECK in SQL Server, and MySQL options."
sources:
  - https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-DESC-VALIDATE-CONSTRAINT
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/disable-foreign-key-constraints-with-insert-and-update-statements
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html#online-ddl-foreign-key-operations
  - https://www.postgresql.org/docs/16/sql-altertable.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adding constraints safely (NOT VALID / VALIDATE)

Adding a constraint normally scans the whole table to check existing rows while holding a lock
that blocks writes (or everything). On a large table that is an outage.

## PostgreSQL: two steps
```sql
-- 1. Instant: enforce for new/changed rows only (brief lock; checked on PostgreSQL 16.4: pg_constraint.convalidated = f afterwards and a violating insert fails immediately)
SET lock_timeout = '3s';
ALTER TABLE orders ADD CONSTRAINT orders_customer_fk
  FOREIGN KEY (customer_id) REFERENCES customers(id) NOT VALID;
ALTER TABLE orders ADD CONSTRAINT orders_amount_positive CHECK (amount >= 0) NOT VALID;

-- 2. Later: check existing rows with SHARE UPDATE EXCLUSIVE (reads and writes continue)
ALTER TABLE orders VALIDATE CONSTRAINT orders_customer_fk;
ALTER TABLE orders VALIDATE CONSTRAINT orders_amount_positive;
```
Fix violating rows between the steps (VALIDATE fails and reports a violating row otherwise):
`SELECT o.id FROM orders o LEFT JOIN customers c ON c.id = o.customer_id WHERE c.id IS NULL AND o.customer_id IS NOT NULL;`

**NOT NULL** without a long scan (PG12+):
```sql
ALTER TABLE orders ADD CONSTRAINT orders_region_nn CHECK (region IS NOT NULL) NOT VALID;
ALTER TABLE orders VALIDATE CONSTRAINT orders_region_nn;
ALTER TABLE orders ALTER COLUMN region SET NOT NULL;   -- uses the valid CHECK, skips the scan (confirmed on 16.4 with client_min_messages=debug1: "existing constraints on column ... are sufficient to prove that it does not contain nulls")
ALTER TABLE orders DROP CONSTRAINT orders_region_nn;
```
(PG18 adds `NOT NULL ... NOT VALID` directly (gated: unconfirmed, source is paywalled or blocked))

**UNIQUE**: `CREATE UNIQUE INDEX CONCURRENTLY`, then `ADD CONSTRAINT ... UNIQUE USING INDEX` (both ran on 16.4).

## SQL Server
```sql
ALTER TABLE dbo.Orders WITH NOCHECK ADD CONSTRAINT FK_Orders_Customers
  FOREIGN KEY (CustomerId) REFERENCES dbo.Customers(Id);
-- later, in a window (scans, blocks writes during the check):
ALTER TABLE dbo.Orders WITH CHECK CHECK CONSTRAINT FK_Orders_Customers;
```
A `WITH NOCHECK` constraint is **not trusted** (gated: unconfirmed, source is paywalled or blocked) (`sys.foreign_keys.is_not_trusted = 1`) and the
optimizer cannot use it for join elimination; validate when you can.

## MySQL
Adding a FK with `foreign_key_checks = 0` uses INPLACE without validating existing rows (the
same trust problem: data is never checked). CHECK constraints (8.0.16+) are validated with a
table copy; use gh-ost/pt-osc for big tables, or `NOT ENFORCED` first (gated: unconfirmed, source is paywalled or blocked).

## Rollout order (expand/contract)
1. Application stops writing violating data (deploy code first).
2. Add the constraint unvalidated.
3. Backfill/clean existing data in batches.
4. Validate.

## Verify
PostgreSQL: `SELECT conname, convalidated FROM pg_constraint WHERE conrelid = 'orders'::regclass;`
shows `true`; SQL Server: `is_not_trusted = 0`; violating inserts now fail.
