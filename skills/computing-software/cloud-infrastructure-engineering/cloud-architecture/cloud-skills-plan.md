---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-skills-plan
name: cloud-skills-plan
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-strategy, cloud-skills-plan, skills-readiness, training-plan, certification]
level: practitioner
status: draft
description: "Build a cloud skills readiness plan: role-based skills matrix, gap assessment, learning paths, certifications, hands-on practice and hiring mix."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/plan/adapt-roles-skills-processes", "https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/people-perspective.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud skills readiness plan

## Steps
1. **Define roles** affected: cloud architect, platform engineer, developer, SRE/operations,
   security engineer, network engineer, data engineer, FinOps analyst, product owner,
   finance partner, procurement.
2. **Skills matrix** per role with target proficiency (aware, practitioner, expert) across:
   provider fundamentals, IaC, networking, identity, security, containers, CI/CD,
   observability, cost management, the chosen managed services.
3. **Assess current levels** via self-assessment plus manager calibration or practical
   tests; produce a heat map of gaps by team and timing relative to the migration plan.
4. **Learning paths**: provider learning portals and certifications (foundational for all,
   associate/professional for technical roles), internal workshops on the landing zone,
   sandbox accounts with budgets, pairing with experienced engineers, game days.
5. **Timing**: train each team just before its workloads migrate; skills decay unused.
6. **Build vs buy**: hire or contract scarce expertise to seed teams, with knowledge
   transfer obligations.
7. **Track**: proficiency movement, certifications, and outcome metrics (incidents caused
   by misconfiguration, time to first deploy).

## Gotchas
- Certification counts are a weak proxy; hands-on delivery matters more.
- Ignoring finance and procurement skills causes FinOps and contract problems later.

## Verify
- [ ] Gap heat map exists and links to the migration timeline.
- [ ] Every engineer has sandbox access and a learning path.
