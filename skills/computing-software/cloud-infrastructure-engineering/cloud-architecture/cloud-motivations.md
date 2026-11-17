---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-motivations
name: cloud-motivations
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-strategy, cloud-motivations, caf-strategy, migration-motivations, innovation-motivations, critical-business-events]
level: intro
status: draft
description: "Capture and prioritise cloud adoption motivations (critical events, migration, innovation) with stakeholders as CAF Strategy recommends, so the plan optimises for the real driver."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/", "https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/business-perspective.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Documenting cloud adoption motivations

## Motivation groups (CAF)
- **Critical business events**: datacenter exit/lease end, end of support for OS/DB, merger or
  divestiture, regulatory change, capacity crisis.
- **Migration motivations**: cost savings, reduced vendor/technical complexity, IT operating
  efficiency, scale, security/compliance posture.
- **Innovation motivations**: faster time to market, new customer experiences, data and AI,
  global reach, transforming products.

## Steps
1. Interview the executive sponsor and key business/IT leaders; capture motivations verbatim.
2. Classify, then force-rank: which one would make the programme a success on its own?
3. Translate the top ones into business outcomes and measurable KPIs.
4. Note the implication on approach:
   - Critical event -> speed, rehost first, fixed deadline.
   - Cost -> rationalisation, rightsizing, FinOps from day one.
   - Innovation -> modernise selected apps, platform engineering, data.
5. Share the ranked list so teams resolve trade-offs consistently.

## Gotchas
- "All of the above": unranked motivations produce contradictory decisions (e.g. rehost for speed
  vs refactor for innovation).
- Cost savings promised from rehost alone are rarely realised.

## Verify
- [ ] Ranked motivations signed by the sponsor.
- [ ] Each top motivation linked to KPIs.
