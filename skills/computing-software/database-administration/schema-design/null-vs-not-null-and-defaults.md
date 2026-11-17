---
id: computing-software.database-administration.schema-design.null-vs-not-null-and-defaults
name: null-vs-not-null-and-defaults
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, nullability, not-null, default-values, missing-data, data-types]
level: practitioner
status: verified
description: "Decide column nullability and defaults deliberately: what NULL should mean, NOT NULL by default, sentinel values to avoid, adding NOT NULL columns safely, and defaults per engine."
sources:
  - https://www.postgresql.org/docs/current/ddl-default.html
  - https://www.postgresql.org/docs/current/sql-altertable.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/specify-default-values-for-columns
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NULL vs NOT NULL and defaults

## Default to NOT NULL
Make every column `NOT NULL` unless "unknown/not applicable" is a real state the business needs. Nullable columns spread three-valued logic into every query (`<>` silently excludes NULLs), complicate uniqueness, and hide missing data bugs.

## When NULL is right
- Genuinely unknown or not-yet-known values: `shipped_at` until shipping, `end_date` for open ranges, `middle_name` when not provided.
- Optional foreign keys (`manager_id` for the CEO).
Document what NULL means per column ("NULL = not shipped yet"). If a column has two different "missing" meanings (unknown vs not applicable), model them explicitly (status column or separate table).

## Avoid sentinel values
`'1900-01-01'`, `-1`, `''`, `'N/A'` instead of NULL break aggregates (averages include -1), sorting and FK semantics. Use NULL or a proper status.

## Defaults
```sql
created_at timestamptz NOT NULL DEFAULT now(),
status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','paid','cancelled')),
is_active boolean NOT NULL DEFAULT true,
id uuid NOT NULL DEFAULT gen_random_uuid()
```
- A default applies only when the column is omitted from INSERT; explicit `NULL` still violates NOT NULL (good).
- Do not use defaults to paper over missing application data (`DEFAULT ''` for required names).

## Adding a NOT NULL column to a big table
- PostgreSQL 11+: `ADD COLUMN c int NOT NULL DEFAULT 0` avoids a table rewrite when the default is a constant (11 release notes); volatile defaults such as `random()` still need the rewrite.
- MySQL and SQL Server have their own fast-add-column rules (MySQL `ALGORITHM=INSTANT`): check the Online DDL / ALTER TABLE docs for your version.
- Making an existing column NOT NULL: backfill in batches, then PostgreSQL `ADD CONSTRAINT c_not_null CHECK (c IS NOT NULL) NOT VALID`, `VALIDATE CONSTRAINT`, then `SET NOT NULL` (the sequence runs on 18; PG12 release notes: `SET NOT NULL` avoids the scan when existing constraints prove no nulls, the CHECK form is the documented trick in the ALTER TABLE page).

## Engine quirks
- Oracle and MySQL have NULL/empty-string and strict-mode quirks (Oracle treats `''` as NULL; MySQL non-strict modes coerce invalid values): confirm in their docs and run MySQL with strict `sql_mode`.
- SQLite allows NULL in a PRIMARY KEY column unless it is `INTEGER PRIMARY KEY`, WITHOUT ROWID, STRICT, or declared NOT NULL (SQLite CREATE TABLE docs; two NULL inserts into `a TEXT PRIMARY KEY` succeeded on 3.50.4); declare NOT NULL.

## Verify
Query the catalog for nullable columns (`information_schema.columns WHERE is_nullable = 'YES'`) and confirm each has a documented reason.
