---
id: computing-software.database-administration.schema-design.booleans-and-status-flags
name: booleans-and-status-flags
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, boolean-columns, status-flags, state-machine, enums, data-types]
level: practitioner
status: gated
description: "Model booleans and status correctly: native boolean types per engine, when several flags should become one status or timestamp column, and indexing low-cardinality flags."
sources:
  - https://www.postgresql.org/docs/current/datatype-boolean.html
  - https://dev.mysql.com/doc/refman/8.4/en/numeric-type-syntax.html
  - https://learn.microsoft.com/en-us/sql/t-sql/data-types/bit-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Booleans and status flags

## Types per engine
| Engine | Boolean |
|---|---|
| PostgreSQL | `boolean` (true/false/NULL) |
| MySQL | `BOOLEAN` is a synonym for `TINYINT(1)`; zero is false, nonzero is true (so `2 = TRUE` is false); add `CHECK (flag IN (0,1))` (CHECK is enforced from 8.0.16, earlier versions parsed and ignored it) |
| SQL Server | `bit` (0/1/NULL); 8 or fewer bit columns in a table are stored as 1 byte, 9 to 16 as 2 bytes |
| Oracle | SQL `BOOLEAN` is listed in the current Oracle SQL reference (the first release is not confirmed here: check the release notes); where it is unavailable use `NUMBER(1) CHECK (x IN (0,1))` or `CHAR(1) CHECK (x IN ('Y','N'))` |
| SQLite | integer 0/1 (`TRUE`/`FALSE` keywords since 3.23.0; `2 IS TRUE` is 1 but `2 = TRUE` is 0) |

Make flags `NOT NULL DEFAULT false` unless "unknown" is meaningful; three-state booleans confuse everyone.

## Flag explosion smell
```sql
is_paid boolean, is_shipped boolean, is_cancelled boolean, is_refunded boolean
```
Allows impossible combinations (shipped and cancelled and not paid). Replace with a single status (lookup table FK or constrained text/enum) representing a state machine, enforced by CHECK or transition rules:
```sql
status text NOT NULL DEFAULT 'pending'
  CHECK (status IN ('pending','paid','shipped','cancelled','refunded'))
```

## Timestamp instead of boolean
`is_deleted` → `deleted_at timestamptz NULL`; `is_verified` → `verified_at`. You get the fact and when it happened, at no extra cost. Query `WHERE deleted_at IS NULL`.

## Indexing flags
A plain index on a boolean is rarely useful (50/50 split → scan is cheaper). Useful when one value is rare and queried:
```sql
CREATE INDEX ON jobs (created_at) WHERE NOT processed;           -- PostgreSQL partial index
CREATE INDEX ix_jobs_pending ON dbo.jobs (created_at) WHERE processed = 0;   -- SQL Server filtered (unrun: no SQL Server here; gated: unconfirmed, source is paywalled or blocked))
```
In MySQL (partial indexes are not confirmed here: check the CREATE INDEX manual page), put the flag as the leading column of a composite with the sort column: `(processed, created_at)`.

## Bitmask columns
Packing many flags into one integer (`permissions & 4`) saves bytes but defeats indexes and readability; use a child table (`user_permissions`) or a set of booleans unless storage is extreme.

## Verify
Check there are no rows in impossible flag combinations (`WHERE is_shipped AND is_cancelled`) before migrating to a status column; afterwards CHECK prevents them.
