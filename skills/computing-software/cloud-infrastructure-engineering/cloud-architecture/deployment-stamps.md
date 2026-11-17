---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.deployment-stamps
name: deployment-stamps
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, design-patterns-cloud, deployment-stamps, scale-units, multitenancy, tenant-routing, stamp-capacity, geode, sovereign-deployment]
level: advanced
status: docs-checked
description: "Scale a multi-tenant system by deploying identical independent stamps: capacity, tenant-to-stamp routing, infrastructure as code, staged rollout, tenant moves and drift."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/deployment-stamp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deployment stamps (scale units)

A stamp (also service unit, scale unit or cell) is an independent copy of the application components, including data stores, deployed as one group. In a multitenant solution each stamp serves a predefined set of tenants; add stamps to scale almost linearly, span regions and separate customer data. A region can hold one or several stamps. Stamps implicitly shard data.

## Use when
- Natural scale limits exist (connections, host names, sockets) or scale-up gets prohibitively expensive versus scale-out.
- Some tenants need isolation, different versions, different update cadence (stamps can implement deployment rings), or specific regions for latency or data sovereignty.
- You want blast-radius containment: an outage in one stamp leaves tenants on others unaffected.

Not suited to simple solutions, systems that scale within one instance, needs to replicate data across all instances (use the Geode pattern), scaling only some components (consider sharding), or static content only.

## Steps
1. **Define capacity** with a proxy metric such as tenants per stamp, found by load testing; instrument each stamp, monitor used versus available capacity and deploy new stamps proactively so you can direct new tenants to them.
2. **Describe each stamp as code** (Bicep or Terraform) so deployment is repeatable and configuration cannot drift by hand. Deploy at least two stamps, since a single stamp lets single-instance assumptions creep in.
3. **Route traffic.** Either clients connect to a per-stamp name (for example DNS records like `unit1.aus.myapi.contoso.com`, using a consistent subdomain convention), or a traffic routing service resolves tenant to stamp and either redirects (HTTP 302) or reverse-proxies. A central router is complex and must be highly available: deploy it in multiple regions with a synced tenant-to-stamp store. In the Azure example, API Management looks up the mapping in a geo-replicated Cosmos DB collection and Front Door sends users to the nearest API Management gateway. The router can also offload token validation, throttling and authorisation.
4. **Roll out** to all stamps in parallel or progressively, orchestrated by a release tool such as Azure Pipelines or GitHub Actions. A subscription usually holds all stamps, but subscription-wide service quotas may force several. Use one resource group for all stamps if they update together (tag by stamp), or one per stamp if independent; consider a deployment stack per independently managed stamp and keep shared services outside so retiring a stamp does not remove them. Check what-if results before updating a stack, and move tenants and preserve data before retiring a stamp.
5. **Moving tenants** between stamps is hard: custom logic to transmit tenant data and remove it from the original, possibly via a backplane between stamps.

## Gotchas
- Cost rises substantially because infrastructure is duplicated.
- Counting customers or reporting across stamps means querying each stamp or publishing to a central data warehouse.
- Stamps are not inherently redundant across regions: tenants on a lost region's stamps are down until recovery or migration, so document recovery and consider geo-redundant placement for critical tenants.
- Observability and governance get harder as stamps multiply; collect and correlate telemetry across stamps and validate drift with a policy-as-code tool such as Azure Policy.
- Shared components (a single-page app, for example) can be hosted once and cached globally.
- Geodes differ: any geode serves any user; the two can be combined (the router itself can be a geode).

## Verify
- [ ] A new stamp is provisioned end to end from code.
- [ ] Losing one stamp affects only its tenants (game day).
- [ ] Per-stamp utilisation is visible with enough lead time to add the next stamp.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-region-high-availability-design

## Checked
2026-11-08, documentation only.
Confirmed against: Azure Architecture Center, Deployment Stamps pattern (last updated 2026-04-30), read in full.
Removed as unconfirmed: the "fill to about 70 percent" target, `{tenantId, stampId}` catalogue field names, canary-stamp and bake-time rollout specifics, write-freeze tenant moves, dedicated-stamp product tier advice, the "under a day" provisioning target; the second listed source (multitenant approaches overview) was dropped because it was a short landing page that supports none of the remaining claims.
Method: documentation only; no commands were run.
