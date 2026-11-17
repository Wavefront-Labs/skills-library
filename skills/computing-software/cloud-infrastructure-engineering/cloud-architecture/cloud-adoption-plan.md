---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-adoption-plan
name: cloud-adoption-plan
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-strategy, cloud-adoption-plan, digital-estate, cloud-adoption-framework, migration-backlog]
level: practitioner
status: draft
description: "Build a cloud adoption plan from the digital estate: workload inventory, rationalisation decisions, prioritised backlog, skills and timeline."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/plan/", "https://learn.microsoft.com/azure/cloud-adoption-framework/digital-estate/", "https://learn.microsoft.com/azure/cloud-adoption-framework/plan/template"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud adoption plan and digital estate

## Steps
1. **Digital estate inventory**: workloads (not just servers) with owners, assets, data,
   dependencies, criticality and cost. Use discovery tooling plus the CMDB and owner interviews.
2. **Rationalise** each workload with the Rs (retire, retain, rehost, replatform, refactor,
   rearchitect, rebuild, repurchase/replace with SaaS); record reason.
3. **Align priorities** with business outcomes and constraints: datacentre exit dates,
   licence renewals, hardware refresh, regulatory deadlines.
4. **Build the backlog**: epics per workload or wave, features for assessment, migration,
   optimisation and decommission; estimates in ranges.
5. **Readiness work** ahead of workloads: landing zone, identity, connectivity, governance,
   skills plan, operating model.
6. **Timeline**: waves sequenced by dependency and risk (start with low-risk,
   high-learning workloads), with capacity per wave.
7. **Governance**: steering cadence, KPIs (workloads migrated vs plan, cost vs forecast,
   outcomes), re-planning rule each quarter.

## Gotchas
- Inventories of servers without workload grouping produce plans nobody can own.
- Plans that ignore decommissioning leave double running costs.

## Verify
- [ ] Every workload has a rationalisation decision and owner.
- [ ] Backlog includes decommission items with dates.
