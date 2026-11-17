---
id: computing-software.database-administration.schema-design.normalisation-keys-and-constraints
name: normalisation-keys-and-constraints
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, data-modelling, relational-design, normalisation, normalization, 1nf, 2nf, 3nf, bcnf, denormalisation, primary-key, surrogate-key, natural-key, uuid, uuidv7, identity-column, foreign-key, unique-constraint, check-constraint, not-null, soft-delete, partial-index, expand-contract, zero-downtime-migration, schema-migration, flyway, liquibase, postgresql, mysql, sql-server]
level: practitioner
status: draft
description: "Practical normalisation to 3NF, surrogate vs natural keys, enforcing integrity with PK/FK/unique/check constraints, soft-delete trade-offs and expand/contract migrations."
sources:
  - https://www.postgresql.org/docs/current/ddl-constraints.html
  - https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html
  - https://martinfowler.com/bliki/ParallelChange.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Normalisation, keys and constraints — let the database refuse bad data

**Goal:** a relational schema where each fact lives in one place, every rule that can
be declared is declared, and changes ship without downtime.

## 1. Normal forms, the practical version
- **1NF:** one value per column. No `tags = 'a,b,c'`, no `phone1, phone2, phone3`.
  Use a child table (or a native array/JSON column only if you never join or constrain
  on its elements).
- **2NF/3NF:** every non-key column depends on the key, the whole key, and nothing but
  the key. Test: "if this value changes, how many rows must I update?" If
  `customer_email` sits on `orders`, the answer is "all of that customer's orders":
  move it to `customers`.
Denormalise deliberately, for measured read paths: snapshot values that *should* be
frozen (price at time of order is a different fact from the current price, so storing it
is correct, not denormalisation), materialised views, or summary tables with a stated
refresh owner.

## 2. Keys
| | Surrogate (`bigint identity`, UUID) | Natural (`iso_country_code`, `sku`) |
|---|---|---|
| Stability | never changes | can change (emails, SKUs renamed) |
| Size/joins | small, fast | often wide strings |
| Meaning | none: needs a separate unique constraint | self-describing |
Default: surrogate primary key **plus** a `UNIQUE` constraint on the natural key. The
surrogate alone lets duplicates in. Natural PKs suit stable, standard codes (currency,
country).

Surrogate choice:
- `bigint GENERATED ALWAYS AS IDENTITY` (Postgres/SQL Server/Oracle) or
  `BIGINT AUTO_INCREMENT` (MySQL). Use `bigint`, not `int`: running out of int at
  2.1 billion is a real outage.
- UUIDs when IDs are generated client-side or across shards. Prefer time-ordered
  **UUIDv7**; random v4 keys scatter inserts across a clustered B-tree (bad for InnoDB
  and SQL Server clustered indexes). Store as native `uuid`/`BINARY(16)`, not text.
  Native generation support varies (Postgres 18 adds `uuidv7()`; check your engine).

## 3. Declare the rules
```sql
CREATE TABLE orders (
  id           bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id  bigint NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
  status       text   NOT NULL DEFAULT 'new'
               CHECK (status IN ('new','paid','shipped','cancelled')),
  total_cents  bigint NOT NULL CHECK (total_cents >= 0),
  placed_at    timestamptz NOT NULL DEFAULT now(),
  external_ref text,
  UNIQUE (customer_id, external_ref)
);
CREATE INDEX ON orders (customer_id);   -- FKs are NOT auto-indexed in Postgres/SQL Server
```
- `NOT NULL` by default; nullable only when "unknown" is a real state.
- Money as integer minor units or `numeric(p,s)`, never float.
- Index FK columns; otherwise deletes on the parent scan the child and joins suffer.
  MySQL InnoDB creates them automatically.
- `ON DELETE CASCADE` only for true ownership (order → line items); `RESTRICT` elsewhere.
- MySQL enforces `CHECK` only from 8.0.16; earlier versions parse and ignore it.
- Timestamps with time zone (`timestamptz`, `datetimeoffset`), stored in UTC.

## 4. Soft delete trade-offs
`deleted_at timestamptz NULL` keeps history and allows undo, but:
- Every query must filter it; one forgotten `WHERE` leaks "deleted" data.
- Unique constraints break (a deleted user's email blocks re-signup). Fix with a
  partial unique index: `CREATE UNIQUE INDEX ON users (email) WHERE deleted_at IS NULL;`
  (MySQL has no partial indexes; use a generated column trick or real deletes.)
- FKs still point at soft-deleted rows; cascades don't fire.
- Privacy law erasure requests still need hard deletes.
Alternatives: hard delete plus an audit/history table (trigger or CDC), or move rows to
an archive table. Choose soft delete only when undo is a product feature.

## 5. Changing schemas: expand/contract
Never rename or retype a column in one step while old code runs. Instead:
1. **Expand:** add the new column/table (nullable or with a default; fast metadata-only
   in Postgres 11+ and MySQL 8 `INSTANT`).
2. Deploy code that writes both old and new.
3. **Backfill** in batches (e.g. 5–10k rows per transaction) to avoid long locks and
   replica lag.
4. Switch reads to the new column; add `NOT NULL`/constraints. In Postgres add them
   `NOT VALID` then `VALIDATE CONSTRAINT` to avoid a long exclusive lock.
5. **Contract:** stop writing the old column, then drop it in a later release.
Build indexes online (`CREATE INDEX CONCURRENTLY`, `ONLINE = ON` in SQL Server
Enterprise, InnoDB online DDL). Set a `lock_timeout` on migrations so a blocked DDL fails
fast instead of queueing every query behind it. Version migrations with a tool
(Flyway, Liquibase, Alembic).

## Verify
- [ ] No column stores a list or a fact that belongs to another entity.
- [ ] Every table has a PK; every natural identifier has a `UNIQUE` constraint.
- [ ] FKs are declared and indexed; `CHECK`/`NOT NULL` cover documented business rules.
- [ ] Soft-delete tables use partial unique indexes and a tested default filter.
- [ ] The last migration followed expand/contract and ran with a `lock_timeout`.
