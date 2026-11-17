---
id: computing-software.cybersecurity-defensive.security-architecture.multi-tenant-saas-isolation
name: multi-tenant-saas-isolation
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [security-architecture, tenant-isolation, multi-tenancy, row-level-security, silo-pool-bridge, cross-tenant-access, saas-architecture]
level: advanced
status: draft
description: "Design and verify tenant isolation in multi-tenant SaaS: silo, pool and bridge models, tenant context propagation, row-level security, per-tenant keys, and cross-tenant tests."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/saas-architecture-fundamentals/tenant-isolation.html", "https://www.postgresql.org/docs/current/ddl-rowsecurity.html", "https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-tenant SaaS isolation

A cross-tenant data leak is the defining failure of a SaaS company. Isolation must be enforced by
architecture, not by every developer remembering a `WHERE tenant_id = ?`.

## Models
- **Silo**: dedicated stack/account/database per tenant. Strongest isolation, highest cost; for
  regulated or large tenants.
- **Pool**: shared infrastructure and tables, tenant ID on every row. Cheapest; isolation depends on code.
- **Bridge/hybrid**: shared compute, per-tenant schema or database; or pool for most, silo for premium.

## Enforcement layers
1. **Tenant context from authentication**: tenant ID comes from a verified token claim, never from a
   request parameter or header the client controls.
2. **Propagation**: middleware sets tenant context for the request; downstream services receive it in
   signed tokens, not plain headers.
3. **Data layer guardrails**:
   - PostgreSQL row-level security:
     ```sql
     ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
     CREATE POLICY tenant_isolation ON invoices
       USING (tenant_id = current_setting('app.tenant_id')::uuid);
     -- per request: SET app.tenant_id = '<from token>';  (app role must not be table owner or BYPASSRLS)
     ```
   - ORMs with global tenant filters; repository layer that cannot run unscoped queries.
   - Silo: per-tenant database credentials; connection routing by tenant.
4. **Cloud IAM scoping**: per-tenant IAM roles assumed with session tags (`aws:PrincipalTag/tenant`)
   and resource policies keyed on tenant prefixes (S3 `tenant-123/*`).
5. **Encryption**: per-tenant data keys (envelope encryption) so a tenant can be crypto-shredded and
   keys cannot decrypt another tenant's data; optional customer-managed keys.

## Other shared resources
Caches (key prefix with tenant ID), search indexes (filtered aliases or per-tenant indexes), queues,
file storage, logs and analytics, background jobs (carry tenant context explicitly), noisy-neighbour
limits (per-tenant rate limits/quotas).

## Testing
- Automated cross-tenant tests: tenant A's token requests tenant B's object IDs on every endpoint
  (IDOR suite) and must get 404/403.
- Fuzz IDs and check list endpoints never leak foreign rows.
- Pentests with two tenant accounts as a standard scope item.

## Gotchas
- Admin/support tooling often bypasses tenant filters; audit and restrict it.
- Exports, reports and background jobs are the usual leak paths, not the main API.
- Connection pooling with session variables (RLS) must reset tenant context per checkout.

## Verify
The cross-tenant test suite runs in CI on every endpoint; a query run as the app role without tenant
context returns zero rows.
