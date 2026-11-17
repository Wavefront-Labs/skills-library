---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-kpis
name: architecture-kpis
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-vision, architecture-kpis, value-propositions, togaf-phase-a, outcome-metrics, cloud-business-outcomes, baseline-measures]
level: practitioner
status: draft
description: "Define value propositions and measurable KPIs for a target cloud architecture (baseline, target, owner, data source) so the vision can be verified after delivery."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap03.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/business-outcomes/", "https://dora.dev/guides/dora-metrics-four-keys/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Value propositions and KPIs for the target architecture

## Steps
1. For each stakeholder group, state the value proposition in one sentence ("Product teams ship
   weekly instead of quarterly without new infrastructure tickets").
2. Translate into KPIs with: name, definition, formula, **baseline** (measured now), target,
   date, owner, data source. No baseline = cannot prove value.
3. Mix categories:
   | Category | Example KPI |
   |---|---|
   | Financial | Infrastructure cost per transaction; % spend under commitment |
   | Agility | Lead time for changes; environment provisioning time |
   | Reliability | SLO attainment; MTTR; RTO met in drills |
   | Security/compliance | % resources compliant with baseline; critical vulns > 30 days |
   | Sustainability | kgCO2e per unit of work |
4. Limit to the handful the sponsor will actually review.
5. Put KPIs in the vision and the architecture contract; schedule measurement (Phase G/H).

## Gotchas
- Vanity KPIs ("number of apps migrated") without outcome KPIs.
- Cost KPIs that ignore growth; use unit cost, not total cost.
- Targets set without the owner agreeing they are achievable.

## Verify
- [ ] Each KPI has a measured baseline and a named owner.
- [ ] Dashboard or report scheduled before delivery starts.
