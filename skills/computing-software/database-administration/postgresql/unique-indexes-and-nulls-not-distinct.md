---
id: computing-software.database-administration.postgresql.unique-indexes-and-nulls-not-distinct
name: unique-indexes-and-nulls-not-distinct
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres-index-types, unique-index, nulls-not-distinct, unique-constraint, partial-index, deferrable-constraint]
level: practitioner
status: verified
description: "Enforce uniqueness correctly in PostgreSQL: constraint vs unique index, NULL handling and NULLS NOT DISTINCT, partial unique indexes, deferrable checks and online creation."
sources:
  - https://www.postgresql.org/docs/current/indexes-unique.html
  - https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS
  - https://www.postgresql.org/docs/current/sql-createindex.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unique indexes and NULLS NOT DISTINCT

## Constraint or index
`UNIQUE` constraints are implemented by a unique B-tree index. Prefer the **constraint** when a
foreign key must reference the columns or you need `DEFERRABLE`; use a bare **unique index**
when you need expressions or a `WHERE` clause, which constraints cannot have.

## NULLs
By default NULLs are distinct: `(tenant_id, external_ref)` allows unlimited rows with
`external_ref IS NULL`. PG15+:
```sql
ALTER TABLE accounts ADD CONSTRAINT accounts_email_uq UNIQUE NULLS NOT DISTINCT (tenant_id, email);
CREATE UNIQUE INDEX ON accounts (tenant_id, email) NULLS NOT DISTINCT;
```
Before PG15: a partial index for the NULL case, e.g.
`CREATE UNIQUE INDEX ON accounts (tenant_id) WHERE email IS NULL;`.

## Partial and expression uniqueness
```sql
-- one active subscription per customer; cancelled ones unlimited
CREATE UNIQUE INDEX one_active_sub ON subscriptions (customer_id) WHERE status = 'active';
-- case-insensitive email
CREATE UNIQUE INDEX users_email_lower_uq ON users (lower(email));
-- soft delete
CREATE UNIQUE INDEX users_username_live_uq ON users (username) WHERE deleted_at IS NULL;
```
`INSERT ... ON CONFLICT` must name a matching arbiter: `ON CONFLICT (customer_id) WHERE status = 'active' DO NOTHING`.

## Deferrable uniqueness
Shifting values between rows (`UPDATE t SET pos = pos + 1`) fails mid-statement on an ordinary unique constraint (`duplicate key value violates unique constraint`). A `DEFERRABLE` constraint is checked at the end of the statement, so even `INITIALLY IMMEDIATE` lets that single `UPDATE` succeed; `SET CONSTRAINTS ... DEFERRED` extends the check to commit for multi-statement shuffles. Use:
```sql
ALTER TABLE items ADD CONSTRAINT items_pos_uq UNIQUE (list_id, pos) DEFERRABLE INITIALLY IMMEDIATE;
BEGIN; SET CONSTRAINTS items_pos_uq DEFERRED; ...; COMMIT;
```
Deferrable constraints cannot be `ON CONFLICT` arbiters (`ON CONFLICT does not support deferrable unique constraints/exclusion constraints as arbiters`). A partial unique index cannot be the target of a foreign key.

## Adding one to a live table
```sql
CREATE UNIQUE INDEX CONCURRENTLY orders_ref_uq ON orders (external_ref);
ALTER TABLE orders ADD CONSTRAINT orders_ref_uq UNIQUE USING INDEX orders_ref_uq;   -- brief lock
```
If duplicates exist the build fails and leaves an **INVALID** index; drop it, dedupe, retry:
```sql
SELECT external_ref, count(*) FROM orders GROUP BY 1 HAVING count(*) > 1;
```

## Gotchas
- Unique indexes on partitioned tables must include all partition key columns.
- `text` uniqueness respects collation; nondeterministic collations need PG12+ and make
  equality case-insensitive, which may be what you want instead of `lower()`.
- A unique index also serves as a normal index; don't create a second identical B-tree.

## Verify
Attempt a duplicate insert in a transaction and confirm `23505 unique_violation`; check
`pg_index.indisvalid` is true for the index.

## Checked
PostgreSQL 17.6: with the default, two rows `(1, NULL)` are accepted; with `UNIQUE NULLS NOT DISTINCT` the second fails with SQLSTATE 23505, and `CREATE UNIQUE INDEX ... NULLS NOT DISTINCT` builds; the partial index allows many cancelled rows and one active, `ON CONFLICT (customer_id) WHERE status = 'active' DO NOTHING` inserts 0 rows while the same without `WHERE` fails with `there is no unique or exclusion constraint matching the ON CONFLICT specification`; an expression unique index builds (and fails on existing duplicates); the deferrable behaviour and ON CONFLICT error as quoted; a duplicate `CREATE UNIQUE INDEX CONCURRENTLY` fails with `could not create unique index` and leaves `indisvalid = f`, and after deduplication the build and `ADD CONSTRAINT ... UNIQUE USING INDEX` succeed; a foreign key to a partial unique index fails (`there is no unique constraint matching given keys`); a unique index on a partitioned table without the partition key fails (see default-partitions-and-partitioned-indexes).
