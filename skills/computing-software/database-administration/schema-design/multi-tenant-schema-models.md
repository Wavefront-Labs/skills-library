---
id: computing-software.database-administration.schema-design.multi-tenant-schema-models
name: multi-tenant-schema-models
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, schema-patterns, multi-tenant-schema, shared-schema, schema-per-tenant, database-per-tenant, tenant-id, row-level-security, noisy-neighbour]
level: practitioner
status: verified
description: "Choose between shared tables with tenant_id, schema-per-tenant and database-per-tenant, and implement isolation, indexing and migrations for the chosen model."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/saas-tenancy-app-design-patterns
  - https://www.postgresql.org/docs/current/ddl-rowsecurity.html
  - https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/tenant-isolation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-tenant schema models

**Goal:** a tenancy model that matches isolation needs, tenant count and ops capacity, and is hard to get wrong in code.

## The three models
| Model | Isolation | Scale (tenants) | Ops cost | Typical fit |
|---|---|---|---|---|
| Shared schema, `tenant_id` column | Logical (app/RLS) | 100k+ | Lowest | SMB SaaS |
| Schema per tenant (PostgreSQL schemas) | Namespace | Hundreds to low thousands | Migrations x N, catalog bloat | Mid-size B2B |
| Database per tenant | Strong, per-tenant backup/restore/region | Tens to thousands (with automation) | Highest | Enterprise, regulated, data residency |
Hybrid is common: shared for small tenants, dedicated DB for big ones (tenant catalog maps tenant -> connection).

## Shared schema done right
```sql
CREATE TABLE invoices (
  tenant_id bigint NOT NULL REFERENCES tenants(id),
  id bigint GENERATED ALWAYS AS IDENTITY,
  ...,
  PRIMARY KEY (tenant_id, id)
);
CREATE INDEX ON invoices (tenant_id, created_at);
-- composite FKs so a row can only reference rows of the same tenant (checked: a cross-tenant reference is rejected)
ALTER TABLE invoice_lines ADD FOREIGN KEY (tenant_id, invoice_id) REFERENCES invoices (tenant_id, id);
```
- Every index leads with `tenant_id`; every query filters on it.
- Enforce in the database: PostgreSQL RLS policy `USING (tenant_id = current_setting('app.tenant_id')::bigint)` with `SET LOCAL app.tenant_id = '1'` per transaction (works with transaction pooling; checked on 18: `SET LOCAL ROLE` to a non-owner role returned only that tenant's rows, and `SET LOCAL` reverts at commit, after which `current_setting` returns an empty string and the `::bigint` cast errors).
- Partition or shard by `tenant_id` when tables get large.

## Schema / database per tenant
- Migrations must run across all tenants idempotently and track per-tenant versions; a failed tenant must not block others.
- Connection pools multiply per database: use a pooler and keep pool sizes small.
- PostgreSQL with thousands of schemas: measure catalog size and `pg_dump` time before committing to this model.

## Noisy neighbours
Per-tenant rate limits and statement timeouts; move whales to dedicated databases; monitor per-tenant query cost (`pg_stat_statements` won't split by tenant: tag queries via `application_name` or comments).

## Gotchas
- Global unique constraints (e.g. email) become `(tenant_id, email)` unique.
- Reporting across tenants is trivial in shared schema, hard in DB-per-tenant (needs ETL).
- Tenant deletion: shared schema needs cascading deletes in batches; DB-per-tenant is a DROP.

## Verify
An integration test connecting as tenant A cannot read tenant B's rows even when the query forgets the `tenant_id` filter (RLS), and `EXPLAIN` of hot queries shows index access on `(tenant_id, ...)`.
