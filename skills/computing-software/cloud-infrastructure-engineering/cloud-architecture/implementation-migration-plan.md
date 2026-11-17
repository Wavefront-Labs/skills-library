---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.implementation-migration-plan
name: implementation-migration-plan
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, opportunities-and-solutions, implementation-migration-plan, togaf, phase-f, migration-planning, transition-architecture]
level: practitioner
status: draft
description: "Produce the TOGAF Phase F implementation and migration plan: transition architectures, project charters, dependencies, resourcing, costed timeline and risks."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap09.html", "https://pubs.opengroup.org/togaf-standard/adm/chap08.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/plan/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Implementation and migration plan

## Steps
1. **Confirm the transition architectures** (plateaus) from Phase E and what each state looks
   like across business, data, application and technology.
2. **Per project/work package**: scope, deliverables, owner, dependencies, cost, benefits,
   start/end, required resources and skills.
3. **Sequence**: critical path across projects; foundation items (landing zone, identity,
   network, security tooling) before migration waves.
4. **Value per plateau**: each transition must be operable and justify its cost on its own in
   case the programme stops there.
5. **Risks and mitigations**, including interim states (temporary hybrid connectivity, dual
   running costs, interim security controls).
6. **Governance hooks**: architecture contracts per project, review gates, and the
   architecture change process for plan updates.
7. **Get approval** from the steering group and publish the plan in the repository.

## Gotchas
- Dual-running costs of interim states are routinely missing from budgets.
- Plans that assume full availability of key architects slip; check resource contention.

## Verify
- [ ] Costed, sequenced plan with owners and dependencies.
- [ ] Interim states costed and their risks owned.
