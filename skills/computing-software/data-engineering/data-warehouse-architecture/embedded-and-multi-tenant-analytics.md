---
id: computing-software.data-engineering.data-warehouse-architecture.embedded-and-multi-tenant-analytics
name: embedded-and-multi-tenant-analytics
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, embedded-analytics, multi-tenant-analytics, row-level-security, customer-facing-dashboards, signed-embed, tenant-isolation]
level: practitioner
status: draft
description: "Deliver embedded, customer-facing analytics: architecture, tenant isolation, signed embedding, performance SLAs and cost per tenant."
sources:
  - https://learn.microsoft.com/en-us/power-bi/developer/embedded/embedded-row-level-security
  - https://cloud.google.com/looker/docs/single-sign-on-embedding
  - https://docs.snowflake.com/en/user-guide/security-row-intro
  - https://docs.metabase.com/latest/embedding/introduction
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Embedded and multi-tenant analytics

Embedded analytics puts dashboards or charts inside your product for your customers. It's a product feature with SLAs, not an internal BI deployment.

## Architecture options
| Option | Notes |
|---|---|
| Embedded BI tool (Power BI Embedded, Looker embed, Tableau Embedded, QuickSight, Metabase/Superset embedding) | fastest; licensing per capacity/session; theming limits |
| Headless BI / semantic layer + your charts (Cube, dbt Semantic Layer + charting library) | full UX control; more engineering |
| Custom APIs over a serving store (ClickHouse, Druid, Pinot, Postgres aggregates) | best latency at scale; you build everything |

## Tenant isolation (the critical decision)
- **Shared tables + row-level security**: `tenant_id` on every row; security filter injected from the embed token. Simple to operate; one bug leaks data across customers.
- **Schema/database per tenant**: stronger isolation, per-tenant restore and deletion; more objects to manage; cross-tenant benchmarks harder.
- **Hybrid**: shared for small tenants, dedicated for large/regulated ones.
Whatever you pick: the tenant identifier must come from your server-side session, never from client parameters.

## Signed embedding
```text
Your backend authenticates the user -> generates a short-lived signed embed URL/token containing tenant_id and allowed content -> browser loads the iframe/SDK with it.
```
- Power BI: embed token with effective identity (RLS role + username = tenant).
- Looker: signed SSO embed URL with `user_attributes: {tenant_id: ...}` used in access filters.
- Metabase/Superset: JWT-signed embedding with locked parameters.
Keep tokens short-lived (minutes), scope to specific dashboards, rotate signing secrets.

## Performance and SLAs
- Customers expect sub-second to few-second loads: pre-aggregate per tenant/day, cache results (BI cache, CDN for static extracts), use a real-time OLAP store for high concurrency.
- Noisy neighbours: a huge tenant's queries slow everyone in shared compute - route large tenants to dedicated compute or limit query complexity.
- Set and monitor SLOs (p95 dashboard load), per tenant.

## Cost and pricing
- Track cost per tenant (query tags with tenant_id, capacity attribution) to price the feature (tiered analytics add-on) and catch unprofitable tenants.

## Testing isolation
Automated tests log in as tenant A and assert no rows of tenant B are visible on every dashboard and API, including exports and drill-throughs. Pen-test token tampering.

## Verify
- [ ] Cross-tenant access tests pass in CI; tenant_id always derived server-side.
- [ ] p95 load time per tenant within SLO; cost per tenant reported.
