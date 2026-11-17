---
id: computing-software.database-administration.schema-design.versioned-rows-and-slowly-changing-dimensions
name: versioned-rows-and-slowly-changing-dimensions
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, slowly-changing-dimension, scd-type-2, versioned-rows, temporal-tables, schema-patterns]
level: practitioner
status: gated
description: "Keep history of changing rows with versioned rows and slowly changing dimension types (1, 2, 4, 6), validity ranges, current-row lookups and system-versioned temporal tables."
sources:
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
  - https://mariadb.com/kb/en/system-versioned-tables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Versioned rows and slowly changing dimensions

## SCD types (Kimball)
| Type | Behaviour |
|---|---|
| 0 | Never change (original value) |
| 1 | Overwrite; no history |
| 2 | New row per change with validity range; full history |
| 3 | Extra column for previous value; limited history |
| 4 | Current table + separate history table |
| 6 | 1+2+3 hybrid: type 2 rows plus "current value" column on all versions |

## Type 2 design
```sql
CREATE TABLE customer_versions (
  customer_sk bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,   -- surrogate per version
  customer_id bigint NOT NULL,                                    -- business key
  name text NOT NULL, segment text NOT NULL, city text,
  valid_from timestamptz NOT NULL,
  valid_to timestamptz NOT NULL DEFAULT 'infinity',
  is_current boolean NOT NULL DEFAULT true);
CREATE UNIQUE INDEX ON customer_versions (customer_id) WHERE is_current;      -- one current row
-- PostgreSQL: no overlapping versions
ALTER TABLE customer_versions ADD EXCLUDE USING gist (customer_id WITH =, tstzrange(valid_from, valid_to) WITH &&);
```
The type 2 DDL, the no-overlap exclusion constraint, the one-current-row unique index and the close-and-insert change were run on PostgreSQL 18 (a second current row is rejected). Change procedure (one transaction): close the current row (`valid_to = now(), is_current = false`), insert the new version with `valid_from = now()`. Only create a version when tracked attributes actually change (`IS DISTINCT FROM` comparison).

Queries:
```sql
-- current
SELECT * FROM customer_versions WHERE customer_id = 42 AND is_current;
-- as of a date
SELECT * FROM customer_versions WHERE customer_id = 42 AND valid_from <= $1 AND valid_to > $1;
```
Use half-open ranges (`[from, to)`) so boundaries never overlap or gap. Facts in a warehouse reference `customer_sk` of the version valid at the event time.

## System-versioned temporal tables
Engine-managed history (type 4 style):
```sql
-- SQL Server 2016+ (not run here: no SQL Server available; gated: unconfirmed, source is paywalled or blocked))
ALTER TABLE dbo.customers ADD
  valid_from datetime2 GENERATED ALWAYS AS ROW START HIDDEN NOT NULL DEFAULT SYSUTCDATETIME(),
  valid_to   datetime2 GENERATED ALWAYS AS ROW END HIDDEN NOT NULL DEFAULT CONVERT(datetime2, '9999-12-31 23:59:59.9999999'),
  PERIOD FOR SYSTEM_TIME (valid_from, valid_to);
ALTER TABLE dbo.customers SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.customers_history));
SELECT * FROM dbo.customers FOR SYSTEM_TIME AS OF '2026-01-01';
```
MariaDB `WITH SYSTEM VERSIONING` (gated: unconfirmed, source is paywalled or blocked); Oracle Flashback Data Archive (gated: unconfirmed, source is paywalled or blocked); PostgreSQL via `temporal_tables`-style triggers or extensions. System time records when the database learned a change, not business-effective time (bitemporal needs both).

## Verify
For a sample business key: exactly one current row, versions contiguous (`valid_to` of one = `valid_from` of the next), and as-of queries return one row for any timestamp after creation.
