---
id: computing-software.database-administration.schema-design.candidate-and-alternate-keys
name: candidate-and-alternate-keys
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, candidate-key, alternate-key, natural-key, surrogate-key, keys-normalisation]
level: practitioner
status: gated
description: "Identify candidate keys, choose the primary key, and enforce the remaining alternate keys with UNIQUE constraints so business identifiers stay unique alongside surrogate keys."
sources:
  - https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/unique-constraints-and-check-constraints
  - https://en.wikipedia.org/wiki/Candidate_key
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Candidate and alternate keys

## Terms
- **Candidate key**: a minimal set of columns that uniquely identifies a row (no column can be removed and keep uniqueness). A table can have several.
- **Primary key**: the candidate chosen as the main identifier (referenced by foreign keys).
- **Alternate keys**: the other candidates. They are still keys and must be enforced.

Example `employees`: candidates `employee_id` (surrogate), `(company_id, payroll_number)`, `work_email`.

## The common mistake
Adding a surrogate `id` and forgetting the natural keys:
```sql
CREATE TABLE products (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, sku text, name text);
-- duplicates of sku accumulate silently
```
Enforce alternate keys:
```sql
ALTER TABLE products ADD CONSTRAINT products_sku_key UNIQUE (sku);
ALTER TABLE employees ADD CONSTRAINT employees_company_payroll_key UNIQUE (company_id, payroll_number);
CREATE UNIQUE INDEX employees_email_key ON employees (lower(work_email));     -- case-insensitive key
```

## Finding candidate keys
1. List attributes and ask the business which values identify a thing in the real world (invoice number per company, VIN, ISO code).
2. Check data: `SELECT sku, count(*) FROM products GROUP BY sku HAVING count(*) > 1;` must be empty before adding the constraint.
3. Check minimality: is `(company_id, payroll_number, name)` a key? Yes but not minimal (it is a superkey); `(company_id, payroll_number)` is.
4. Watch scope: uniqueness may be per tenant, per period, or among active rows only (partial unique index `WHERE deleted_at IS NULL`).

## Choosing the primary key
| Natural key as PK | Surrogate PK + alternate keys |
|---|---|
| Meaningful, no extra column | Stable even when business values change |
| Wide/composite keys propagate into every FK | Narrow integer/UUID FKs |
| Painful when the "immutable" value changes (emails, names) | Requires enforcing natural uniqueness separately |

Most OLTP designs: surrogate PK + UNIQUE constraints on all natural candidate keys. Use natural PKs for stable codes (ISO country codes, currency codes) and junction tables.

## NULLs in alternate keys
PostgreSQL UNIQUE allows multiple NULLs (verified: two NULL skus inserted). SQL Server unique constraints allow only one NULL (gated: unconfirmed, source is paywalled or blocked). If the key is mandatory, add NOT NULL; PostgreSQL 15+ `UNIQUE NULLS NOT DISTINCT` treats NULLs as equal (PostgreSQL 15 release notes; the second NULL insert fails on 18).

## Verify
For each table, list candidate keys from the data model and confirm each has a PK or UNIQUE constraint (`information_schema.table_constraints`).
