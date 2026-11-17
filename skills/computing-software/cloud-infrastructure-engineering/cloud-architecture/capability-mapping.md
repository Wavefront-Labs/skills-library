---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.capability-mapping
name: capability-mapping
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, business-architecture, togaf, capability-mapping, business-capability-map, heat-map]
level: practitioner
status: draft
description: "Build a business capability map, heat-map it for cloud investment, and link capabilities to applications and workloads to prioritise migration."
sources: ["https://pubs.opengroup.org/togaf-standard/business-architecture/business-capabilities.html", "https://www.businessarchitectureguild.org/page/BIZBOK"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Business capability mapping

A capability is what the business does (Manage Customer Orders), independent of who does it
or which system supports it. Capabilities are stable; org charts and apps are not.

## Steps
1. **Level 1** (8-15 capabilities): strategic, core, supporting - e.g. Customer Management,
   Product Development, Order Fulfilment, Finance, HR.
2. **Level 2/3** decomposition for the areas in scope only. Name with noun + verb-ing or
   noun + management; no application or department names.
3. **Validate** with business owners: every L2 should be recognisable and non-overlapping.
4. **Map applications** to capabilities (many-to-many). Overlaps reveal rationalisation
   candidates; gaps reveal unsupported capabilities.
5. **Heat-map** each capability on: strategic importance, current performance (pain),
   technical health of supporting apps, cost. Colour red/amber/green.
6. **Use it for cloud decisions**: high importance + poor health = modernise first
   (refactor/re-architect); low importance + adequate = rehost or retire; differentiating
   capabilities warrant build, commodity ones SaaS.

## Gotchas
- Mapping processes or org units instead of capabilities makes the map churn with every reorg.
- Over-decomposing everything to L4 takes months; go deep only where decisions are pending.

## Verify
- [ ] Map reviewed by business owners, not only IT.
- [ ] Each in-scope application linked to at least one capability.
