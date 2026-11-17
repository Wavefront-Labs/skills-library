---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-per-tenant
name: cost-per-tenant
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, unit-economics, cost-per-tenant, cost-per-customer, saas-cost-allocation, usage-metering, pooled-resource-apportionment, tenant-profitability]
level: advanced
status: draft
description: "Compute cost per customer/tenant in SaaS: direct silo costs, apportioning pooled resources by metered usage, shared platform overhead, and validating against total cost."
sources: ["https://www.finops.org/framework/capabilities/unit-economics/", "https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/saas-tenant-isolation-strategies.html", "https://aws.amazon.com/blogs/apn/calculating-tenant-costs-in-saas-environments/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost per customer / tenant

## Three cost layers
1. **Direct (silo)**: resources dedicated to a tenant — tag with `tenant-id` or per-tenant
   accounts/projects; allocation is exact.
2. **Pooled**: shared compute/DB/queues — apportion by a **metered consumption proxy** per tenant:
   requests, CPU-ms (from traces/APM), DB storage per tenant, messages, GB egress.
   Different services can use different proxies.
3. **Shared overhead**: platform, observability, security, non-prod — spread by revenue, by
   pooled-share, or evenly per tenant; disclose the method.

## Steps
1. Instrument tenant id on requests, logs and traces (OpenTelemetry attribute `tenant.id`).
2. Daily aggregate per tenant per service: proxy metric totals.
3. Allocate each pooled service's daily cost proportionally to proxy share.
4. Add direct and overhead; produce `date, tenant, plan, cost, revenue`.
5. Validate: Σ tenant cost = total product cost (no leakage).
6. Use: margin by plan, outlier tenants (cost > price), pricing input, sales discounting floors.

## Gotchas
- Request counts underweight expensive requests; prefer compute time or weighted request classes.
- Storage grows monotonically — include it separately; it's often the long-term driver.
- Privacy: tenant-level cost reports go to finance/product, not broadly.

## Verify
- [ ] Reconciliation Σ tenants = product total within 1%.
- [ ] Top 10 tenants by cost reviewed with product/sales.
