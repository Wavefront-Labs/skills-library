---
id: computing-software.data-engineering.data-warehouse-architecture.multi-tenant-data-platform-design
name: multi-tenant-data-platform-design
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, multi-tenancy, tenant-isolation, row-level-security, platform-design]
level: sme
status: docs-checked
description: "Design multi-tenant data platforms: pooled vs siloed isolation models, tenant keys and row-level security, noisy-neighbour controls, per-tenant cost and compliance."
sources:
  - https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/tenant-isolation.html
  - https://docs.snowflake.com/en/user-guide/security-row-intro
  - https://docs.databricks.com/aws/en/tables/row-and-column-filters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-tenant data platform design

**Goal:** serve many tenants (customers of a SaaS product, or internal business units) from one platform with guaranteed isolation, fair performance and attributable cost.

## Isolation models
| Model | Layout | Pros | Cons |
|---|---|---|---|
| Silo | account/database/project per tenant | strongest isolation, per-tenant keys/regions, easy deletion | many objects, deployments x N, cross-tenant analytics harder |
| Bridge | schema per tenant in shared database | moderate isolation, simple per-tenant grants | schema sprawl, migrations x N |
| Pool | shared tables with `tenant_id` | efficient, one deployment | isolation depends entirely on filters/policies |
Mix: pool for small tenants, silo for large/regulated ones.

## Pooled isolation done right
- `tenant_id` on every table and part of keys; consider it in clustering or partitioning too.
- Row access policies bound to the session's tenant, never relying on application WHERE clauses alone:
```sql
CREATE ROW ACCESS POLICY tenant_rap AS (tid VARCHAR) RETURNS BOOLEAN ->
  EXISTS (SELECT 1 FROM governance.tenant_role_map m
          WHERE m.role_name = CURRENT_ROLE() AND m.tenant_id = tid);   -- Snowflake: map roles to tenants
ALTER TABLE events ADD ROW ACCESS POLICY tenant_rap ON (tenant_id);
```
- Snowflake's page notes that a policy referencing a mapping table can perform worse than a simple policy, and shows memoizable functions as the way to reduce that cost; test at your table sizes.
- Databricks equivalent: Unity Catalog row filters (`ALTER TABLE ... SET ROW FILTER`) are SQL UDFs bound per table; Databricks recommends ABAC policies when you need consistent filtering across many tables. Keep UDFs simple, match UDF parameter types to column types (a mismatch can silently cast to NULL with ANSI mode off, so a filter can return all rows), and note you cannot apply row filters to a view.
- Authentication is not isolation: per the AWS tenant-isolation paper, an authenticated and authorized user can still reach another tenant's resources unless a separate isolation control uses the tenant context to scope access.
- Embedded analytics: pass tenant context (for example claims in a token) and apply it in the BI layer; confirm the policy is also enforced in the warehouse.
- Tests: automated cross-tenant leakage tests in CI (query as tenant A, assert zero rows of B).

## Noisy neighbours
Separate compute per tier or large tenant, query timeouts and concurrency limits; see the serving SLA skill for platform levers.

## Cost attribution
Tag compute with tenant or tenant tier; for pooled compute, apportion by query history (bytes scanned or execution time per tenant from query tags).

## Compliance
- Data residency: region-specific silos for tenants that need them.
- Tenant deletion: pooled tables need delete-by-tenant jobs across all tables and a backups strategy; silos drop the database.
- Per-tenant encryption keys push towards silo.

## Verify
Leakage tests pass for every exposed table; per-tenant cost report sums to the bill; deleting a test tenant removes all its rows.

## Checked
Date: 2026-11-09. Confirmed: the AWS tenant-isolation page (silo versus pooled resources, authentication is not isolation); the Snowflake row access policy page (CURRENT_ROLE conditions, mapping-table subqueries and their performance cost, ALTER TABLE ... ADD ROW ACCESS POLICY ... ON, policy evaluated with the owner's role); the Databricks row-filter page (UDF filters, ABAC recommendation, type-mismatch caveat, no filters on views). The isolation-model table, cost attribution, residency and deletion advice are design guidance not stated by the pages. Removed: Snowflake resource monitors, BYOK wording.
Method: documentation only; no commands were run.
