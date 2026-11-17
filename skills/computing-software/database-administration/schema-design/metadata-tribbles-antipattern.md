---
id: computing-software.database-administration.schema-design.metadata-tribbles-antipattern
name: metadata-tribbles-antipattern
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, metadata-tribbles, table-per-period, sql-antipatterns, partitioning, schema-patterns]
level: practitioner
status: draft
description: "Replace metadata tribbles (orders_2025, orders_2026 tables or column per period) with one table plus partitioning, and migrate data and queries without downtime."
sources:
  - https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/
  - https://www.postgresql.org/docs/current/ddl-partitioning.html
  - https://dev.mysql.com/doc/refman/8.4/en/partitioning.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metadata tribbles (table per year / column per period)

## The antipattern (Karwin)
Data values encoded in table or column names:
- Tables: `bugs_2024`, `bugs_2025`, `customers_eu`, `customers_us`, `tenant_42_orders`.
- Columns: `sales_2024`, `sales_2025`, `revenue_jan`..`revenue_dec`.

Problems: every new period needs DDL; queries spanning periods need UNIONs or dynamic SQL; constraints and uniqueness cannot span tables (an id unique across years?); moving a row between "periods" means delete+insert across tables; schema keeps growing ("tribbles multiply").

## Fix for row-wise tribbles: one logical table, partitioned physically
```sql
CREATE TABLE bugs (
  id bigint GENERATED ALWAYS AS IDENTITY,
  reported_at timestamptz NOT NULL,
  summary text NOT NULL,
  PRIMARY KEY (id, reported_at)
) PARTITION BY RANGE (reported_at);
CREATE TABLE bugs_2025 PARTITION OF bugs FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
CREATE TABLE bugs_2026 PARTITION OF bugs FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
```
Applications see one table; the engine prunes partitions and lets you drop old periods cheaply. Automate partition creation (pg_partman, scheduled job). MySQL `PARTITION BY RANGE`, SQL Server partition functions/schemes, Oracle interval partitioning (creates partitions automatically).

Partitioning is only needed at scale (tens of GB+); below that, one plain table with an index on the date is enough.

## Fix for column-wise tribbles: rows, not columns
```sql
CREATE TABLE monthly_revenue (account_id bigint, month date, revenue numeric(14,2) NOT NULL,
  PRIMARY KEY (account_id, month));
```
Pivot for reports in the query or BI tool.

## Migrating existing per-year tables
1. Create the partitioned table; attach existing tables as partitions where the engine allows (PostgreSQL `ATTACH PARTITION` with a matching CHECK constraint to skip validation).
2. Or create a view `bugs_all` as `UNION ALL` of the old tables to move readers first, then consolidate.
3. Replace dynamic table-name code with predicates on the date column.

## Multi-tenant tribbles
`tenant_42_orders` tables per tenant: use a `tenant_id` column (+ RLS) or schema-per-tenant deliberately, not by accident.

## Verify
`EXPLAIN` of a one-year query on the partitioned table touches one partition; no application code builds table names from dates.
