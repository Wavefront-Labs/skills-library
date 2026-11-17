---
id: computing-software.database-administration.schema-design.enforcing-business-rules-in-the-database
name: enforcing-business-rules-in-the-database
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, business-rules, check-constraints, constraint-triggers, data-integrity, keys-normalisation]
level: practitioner
status: verified
description: "Decide which business rules the database should enforce (NOT NULL, CHECK, UNIQUE, FK, exclusion constraints, triggers) versus the application, with patterns and pitfalls."
sources:
  - https://www.postgresql.org/docs/current/ddl-constraints.html
  - https://www.postgresql.org/docs/current/sql-createtrigger.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/create-check-constraints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enforcing business rules in the database

**Principle:** rules about data validity that must hold regardless of which application, script or admin writes the data belong in the database. Rules about workflow, UX or external systems belong in the application.

## The ladder (strongest, cheapest first)
| Rule | Mechanism |
|---|---|
| Value required | `NOT NULL` |
| Value domain | data type, `CHECK (qty > 0)`, `CHECK (status IN (...))`, domains / lookup table FK |
| Cross-column in a row | `CHECK (end_date IS NULL OR end_date >= start_date)` |
| Uniqueness (incl. conditional) | `UNIQUE`, partial unique index (`WHERE active`) |
| Reference exists | `FOREIGN KEY` with explicit ON DELETE |
| No overlapping ranges | PostgreSQL exclusion constraint |
| Cross-row / cross-table aggregates | trigger, deferred constraint trigger, or serialised application logic |

## Examples
```sql
ALTER TABLE bookings ADD CONSTRAINT bookings_dates CHECK (check_out > check_in);

-- no double booking of a room (PostgreSQL)
CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER TABLE bookings ADD CONSTRAINT no_overlap
  EXCLUDE USING gist (room_id WITH =, daterange(check_in, check_out) WITH &&);

-- "an order must have at least one line" checked at commit
CREATE CONSTRAINT TRIGGER order_has_lines AFTER INSERT OR UPDATE ON orders
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_order_has_lines();
```

## Triggers for cross-row rules: beware concurrency
A trigger that checks `SELECT sum(amount) ... <= limit` can be bypassed by two concurrent transactions each seeing the old sum under READ COMMITTED (reasoning from MVCC visibility; not reproduced here because the embedded build is single-connection). Use `SERIALIZABLE`, lock the parent row (`SELECT ... FOR UPDATE` on the account), or maintain the aggregate in the parent row with a CHECK.

## Name constraints
Named constraints give readable errors that the application can map to user messages: `violates check constraint "bookings_dates"`.

## Adding to existing data
Validate existing rows first or add without validation and validate later (PostgreSQL `NOT VALID` + `VALIDATE CONSTRAINT`, checked on 18; other engines have equivalents such as SQL Server's `WITH NOCHECK`, whose constraints stay untrusted until re-checked: see its docs).

## Engine gaps
- MySQL enforces CHECK only from 8.0.16 (its release notes: earlier versions "parsed and ignored it").
- SQLite enforces CHECK; FKs only with `PRAGMA foreign_keys=ON` (checked on SQLite 3.50: an orphan insert succeeds until the pragma is on; the pragma is a no-op inside an open transaction).

## Verify
For each rule in the data dictionary, a test inserts a violating row and expects the specific constraint error.
